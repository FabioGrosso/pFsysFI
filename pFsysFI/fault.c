
#include <time.h>
#include <stdio.h>
#include <string.h>
#include "log.h"
#include "fault.h"


void inject(Config *config, void *buf, size_t size){
    if (strcmp("bitflip",config->model_name) == 0){
        char * data = parepare_bitflip(buf,size);
        bit_flip(data,config->consecutive_bits);
    }
    if (strcmp("shornwrite", config->model_name) == 0){

    }
}


char* parepare_bitflip(void * buf, size_t size){
    char * buf_char = (char *)(buf);
    int inject_index = generate_random(size);
    char data = buf_char[inject_index];
    return &data;
}

int generate_random(size_t size){
    srand(time(NULL));
    return rand()%size;
}

void bit_flip(char *data, int num_bits){
    srand(time(NULL));
    log_msg("original: %c ",*data);
    size_t offset_start = rand()%(8-num_bits);
    for (int i = 0; i < num_bits; i++){
        *data ^= 1UL << offset_start+i;
    }
    log_msg("after: %c ",*data);
}
