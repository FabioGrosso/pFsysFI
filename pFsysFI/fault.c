
#include <time.h>
#include <stdio.h>
#include <string.h>
#include "log.h"
#include "fault.h"
#include <errno.h>
#include <stdlib.h>
#define CONFIG_FILE "/home/bo/workspace/fifaaficonfig"
#define CONFIG_BITFLIP_FILE "/home/bo/workspace/bitflip"
#define CONFIG_SHORNWRITE_FILE "/home/bo/workspace/shornwrite"

#define SHORNWRITE_THRES 512

int inject(Config config, void *buf, size_t size){
    if (strcmp("bitflip",config.model_name) == 0){
        char * data = prepare_bitflip(buf,size);
        bit_flip(data,config.consecutive_bits);
        return size;
    }
    if (strcmp("shornwrite", config.model_name) == 0){
        size_t new_size = prepare_shornwrite(buf,size,config.shornwrite_portion);
        log_msg("shornwrite: %d %d",new_size,size);
        return new_size;
    }
     if (strcmp("dropwrite", config.model_name) == 0){
         log_msg("dropwrite: 0");
        return 0;
    }
}


char* prepare_bitflip(void * buf, size_t size){
    char * buf_char = (char *)(buf);
    int inject_index = generate_random(size);
    char *data = &buf_char[inject_index];
    return data;
}

int prepare_shornwrite(void *buf, size_t size, float shorn_portion){
    char *buf_char = (char *)(buf);
    int size_new = 0;
    if (size < SHORNWRITE_THRES){
       return size;
    }
    else{
        size_new = size - SHORNWRITE_THRES*(int)(8*(1-shorn_portion));
        return size_new;
    }
}

int generate_random(size_t size){
    srand(time(NULL));
    return rand()%size;
}

void bit_flip(char *data, int num_bits){
    srand(time(NULL));
    log_msg("original: %c ",*data);
    size_t offset_start = rand()%(8-num_bits);
    int i = 0;
    for (i = 0; i < num_bits; i++){
        *data ^= 1UL << offset_start+i;
    }
    log_msg("after: %c ",*data);
}

int load_config(Config *config){
    char *line[5]  = {0};
    size_t len = 0;
    ssize_t read;
    FILE *fp = fopen(CONFIG_FILE,"r");
    FILE *f_spec = NULL;
    if (fp == NULL){
        log_msg("Can not open config file for FIFAA");
        log_msg("fopen failed, errno = %d\n", errno);
        return -1;
    }
    // read line by line
    // 1. error mode
    read = getline(&line[0], &len, fp);
    line[0][strlen(line[0])-1] = '\0';
    config->is_inject = atoi(line[0]);
    log_msg("%d\n",config->is_inject);
    // 2. fault model
    read = getline(&line[1], &len, fp);
    config->model_name = line[1];
    line[1][strlen(line[1])-1] = '\0';
    log_msg("%s\n",config->model_name);
    // 3. op name
    read = getline(&line[2], &len, fp);
    config->op_name  = line[2];
    line[2][strlen(line[2])-1] = '\0';
    log_msg("%s\n",config->op_name);
    // 4. instance
    read = getline(&line[3], &len, fp);
    line[3][strlen(line[3])-1] = '\0';
    config->instance  = atoi(line[3]);
    log_msg("%d\n",config->instance);
    fclose(fp);
    // need to read the spec file 
    if (strcmp("bitflip\0",config->model_name) == 0){
        f_spec = fopen(CONFIG_BITFLIP_FILE,"r");
        if (f_spec == NULL){
            log_msg("Can not open spec file for bitflip");
            return -1;
        }
        log_msg("get into consecutive_bits file");
        read = getline(&line[4], &len, f_spec);
        config->consecutive_bits = atoi(line[4]);
    	log_msg("consecutive bits: %d\n",config->consecutive_bits);
        fclose(f_spec);
    }
    if (strcmp("shornwrite\0", config->model_name) == 0){
        f_spec = fopen(CONFIG_SHORNWRITE_FILE,"r");
        if (f_spec == NULL){
            log_msg("Can not open spec file for shornwrite");
            return -1;
        }
        read = getline(&line[4], &len, f_spec);
    	//line[4][strlen(line[4])-1] = '\0';
    	log_msg("portion: %s\n",line[4]);
        config->shornwrite_portion = (float)atof(line[4]);
        //config->shornwrite_portion = 0.5;
    	log_msg("portion: %f\n",config->shornwrite_portion);
        fclose(f_spec);
    }
    return 0;

}
