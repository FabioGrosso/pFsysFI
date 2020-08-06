import os
import sys
import re
import yaml

OP_PREFIX = 'fifaa_'
OP_MATCHING = OP_PREFIX+r'\(.*?\)'
APP_NAME = "x"

def parse_log(logfile:str) -> dict:

    file_op = {}
    with open(logfile) as f:
        lines = f.readlines()
        for line in lines:
            if OP_PREFIX in line:
                if re.search(OP_MATCHING,line) != None:
                    items = line.split("(")
                    op = items[0]
                    if op not in file_op:
                        file_op[op] = 1
                    else:
                        file_op[op] = file_op[op] + 1
    gen_yaml(file_op,APP_NAME)

def gen_yaml(op_list:dict,app:str):

    with open(app+".yaml", 'w') as y_file:
        documents = yaml.dump(op_list, y_file)


parse_log("fifaa.log")


