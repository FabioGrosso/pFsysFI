#ifndef _FAULT_H_
#define _FAULT_H_

#include "log.h"
#include <exception>
#include <time.h>

using namespace std;

class MyException: public exception
{
  virtual const char* what() const throw()
  {
    return "No support fault model";
  }
} myex;


class FaultModel{
    public:
        FaultModel(std::string name, void *buf, size_t size): model_name_{verify(name), buf_(buf), size_(size)};

        void inject(){
            if (model_name_ == "bitflip"){
                char * data = parepare_bitflip();
                bit_flip(data,2);
            }
            if (model_name_ == "shornwrite"){

            }
        }


    private:

        std::string model_name_;
        void *buf_;
        size_t size_;

        static std::string verify(const std::string name){
            if (name == "bitflip" || 
                name == "shornwrite" ||
                name == "misdirwrite" ||
                name == "droppedwrite" ||
                name == "metadata")
                return name;
            else
                throw myex;
        }

        char* parepare_bitflip(){
            char * buf_char = reinterpret_cast<char*>(buf_);
            inject_index = generate_random(size_);
            char data = buf_char[inject_index];
            return &data;
        }

        size_t generate_random(size_t size){
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
};

#endif