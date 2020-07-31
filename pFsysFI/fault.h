

#ifndef _FAULT_H_
#define _FAULT_H_



typedef struct Configuration{
    const char * model_name;
    int consecutive_bits;
} Config;


int generate_random(int size);


void inject(Config *config, void *buf, int size);

// for bitflip model
char* parepare_bitflip(void * buf, int size);
void bit_flip(char *data, int num_bits);


#endif