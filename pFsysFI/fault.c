
#include <time.h>
#include <stdio.h>
#include <string.h>
#include "log.h"
#include "fault.h"

#define CONFIG_FILE "fiffa.config"

void inject(Config config, void *buf, size_t size){
    if (strcmp("bitflip",config.model_name) == 0){
        char * data = parepare_bitflip(buf,size);
        bit_flip(data,config.consecutive_bits);
    }
    if (strcmp("shornwrite", config.model_name) == 0){

    }
}


char* parepare_bitflip(void * buf, size_t size){
    char * buf_char = (char *)(buf);
    int inject_index = generate_random(size);
    char *data = &buf_char[inject_index];
    return data;
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
    char *line = NULL;
    size_t len = 0;
    ssize_t read;
    FILE *fp = fopen(CONFIG_FILE,"r");
    FILE *f_spec = NULL;
    if (fp == NULL){
        log_msg("Can not open config file for FIFAA");
        return -1;
    }
    // read line by line
    // 1. error mode
    read = getline(&line, &len, fp);
    config->is_inject = atoi(line);
    // 2. fault model
    read = getline(&line, &len, fp);
    config->model_name = line;
    // 3. op name
    read = getline(&line, &len, fp);
    config->op_name  = line;
    // 4. instance
    read = getline(&line, &len, fp);
    config->instance  = atoi(line);
    fclose(fp);
    // need to read the spec file 
    if (strcmp("bitflip",config->model_name) == 0){
        f_spec = fopen(config->model_name,"r");
        if (f_spec == NULL){
            log_msg("Can not open spec file for bitflip");
            return -1;
        }
        read = getline(&line, &len, f_spec);
        config->consecutive_bits = atoi(line);
        fclose(f_spec);
    }
    if (strcmp("shornwrite", config->model_name) == 0){
        f_spec = fopen(config->model_name,"r");
        if (f_spec == NULL){
            log_msg("Can not open spec file for shornwrite");
            return -1;
        }
        read = getline(&line, &len, f_spec);
        config->shornwrite_portion = atof(line);
        fclose(f_spec);
    }
    return 0;

}