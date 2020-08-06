import os
import sys
import re
import yaml

OP_PREFIX = 'fifaa_'
OP_MATCHING = OP_PREFIX+r'.*\(.*?\)'
CONFIG = "config.yaml"

def config_loader(configfile:str):
    yaml_file = open(configfile)
    if yaml_file.closed:
        logging.error("file is not open")
        raise ValueError

    parsed_yaml_loader = yaml.load(yaml_file, Loader=yaml.FullLoader)
    return parsed_yaml_loader

def parse_log(logfile:str,yaml_loader) -> dict:

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
    
    app = yaml_loader["benchmark"]  
    gen_yaml(file_op,app)

def gen_yaml(op_list:dict,app:str):

    with open(app+".yaml", 'w') as y_file:
        documents = yaml.dump(op_list, y_file)

yaml_loader = config_loader(CONFIG)
parse_log("fifaa.log",yaml_loader)


