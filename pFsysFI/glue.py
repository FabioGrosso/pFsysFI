import os
import sys
import re

def read_ptx(f_ptx:str) -> list:
    with open(f_ptx) as ptx:
        lines = ptx.readlines()
        return lines

def remove_extern_block(ptx:list) -> list:

    flag = 0
    new_ptx = []
    for line in ptx:
        if ".extern" in line:
            flag = 1
        if ";" in line:
            flag = 0
        if flag == 1:
            continue
        else:
            new_ptx.append(line)
    print(new_ptx)


ptx = read_ptx("using.ptx")
remove_extern_block(ptx)

