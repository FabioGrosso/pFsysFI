import os
import sys
import re
import yaml
import subprocess
import random
from datetime import datetime

# get the benchmark xml for the profiling data
YAML = ".yaml"
CONFIG = "config"
FS_PREFIX = "fifaa"
OP_MATCHING = FS_PREFIX+"_"+r'.*\(.*?\)'
FS_LOG = FS_PREFIX+".config"
ERROR_FILE = "_ficonfig"


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
    
   return file_op

def gen_yaml(op_list:dict,app:str):

    with open(app+".yaml", 'w') as y_file:
        documents = yaml.dump(op_list, y_file)



def config_loader(configfile:str):
    yaml_file = open(configfile)
    if yaml_file.closed:
        logging.error("file is not open")
        raise ValueError

    parsed_yaml_loader = yaml.load(yaml_file, Loader=yaml.FullLoader)
    return parsed_yaml_loader

def sum_io_calls(file_op:dict)->list:
    
    calls = []
    for op in file_op:
        for i in range(file_op[op]):
            calls.append(op)

    return calls

def random_op(call_ops:list)->str:

    random.seed(datetime.now())
    return random.choice(call_ops)

def get_fault_op(fault_model,fault_op_loader)->list:
    
    if fault_model == "bitflip":
        if "bitflip" not in fault_op_loader:
            logging.error("bitflip fault op not configured")
            raise ValueError
        return fault_op_loader['bitflip']

    if fault_model == "shornwrite":
        if "shornwrite" not in fault_op_loader:
            logging.error("shornwrite fault op not configured")
            raise ValueError
        return fault_op_loader['shornwrite']

def get_target_op(op,file_op)->int:

    total = file_op[op]
    random.seed(datatime.now())
    return random.randint(0,total-1)


def get_inject_model(yaml_loader):

    if 'injection' not in yaml_loader:
        logging.error("injection section not configured")
        raise ValueError
    return yaml_loader['injection']

def get_fault_op(yaml_loader):

    if 'fault_op' not in yaml_loader:
        logging.error("fault op section not configured")
        raise ValueError
    return yaml_loader['fault_op']

def get_injection_flag(injection_loader)->int:

    if 'inject_flag' not in injection_loader:
        logging.error("inject flag params not configured")
        raise ValueError
    return injection_loader['inject_flag']

def get_fault_model(injection_loader)->str:

    if 'fault_model' not in injection_loader:
        logging.error("fault model params not configured")
        raise ValueError
    return injection_loader['fault_model']

def get_injection_trial(injection_loader)->int:

    if 'num_trial' not in injection_loader:
        logging.error("num_trial params not configured")
        raise ValueError
    return injection_loader['num_trial']

def write_to_fuse(error_mode,fault_model,op_name,count):
    with open(FS_PREFIX+ERROR_FILE,'w') as f:
        f.write(error_mode)
        f.write("\n")
        f.write(fault_model)
        f.write("\n")
        f.write(op_name)
        f.write("\n")
        f.write(count)
        f.write("\n")

def get_app(yaml_loader)->str:
    if "benchmark" not in yaml_loader:
        logging.error("benchmark not configured")
        raise ValueError
    return yaml_loader['benchmark']

def get_app_params(yaml_loader)->list:
    if "parameters" not in yaml_loader:
        logging.error("benchmark not configured")
        raise ValueError

    return yaml_loader['parameters']

def get_fault_model_spec(yaml_loader):
    if "fault_model_spec" not in yaml_loader:
        logging.error("benchmark not configured")
        raise ValueError
    return yaml_loader['fault_model_spec']

def get_bitflip_spec(fault_model_spec_loader):
    if "bitflip" not in fault_model_spec_loader:
        logging.error("bitflip spec not configured")
        raise ValueError
    ret = []
    ret.append(fault_model_spec_loader['bitflip']['consecutive_bits'])
    return ret

def get_shornwrite_spec(fault_model_spec_loader):
     if "shornwrite" not in fault_model_spec_loader:
        logging.error("shornwrite spec not configured")
        raise ValueError
    ret = []
    ret.append(fault_model_spec_loader['shornwrite']['shorn_portion'])
    return ret


def write_fault_model_spec(fault_model,specs):
    with open(fault_model,'w') as f:
        for spec in specs:
            f.write(spec)
            f.write("\n")

yaml_loader = config_loader(CONFIG+YAML)
app = get_app(yaml_loader)
params = get_app_params(yaml_loader)
# run profiling to get the fiffa log
execution = []
execution.append(app)
execution.extend(params)
process = subprocess.Popen(execution, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()

if os.path.isfile(FS_LOG) == False:
    print("NO FS LOG FILE FOUND")
    raise ValueError

file_op = parse_log(FS_LOG,yaml_loader)

# obtain the fault injection configuration
fault_op_list = get_fault_op(yaml_loader)

injection_loader = get_inject_model(yaml_loader)

flag = get_injection_flag(injection_loader)

fault_model = get_fault_model(injection_loader)

num_trial = get_injection_trial(injection_loader)

fault_model_spec_loader = get_fault_model_spec(yaml_loader)

# 
for i in range(num_trial):

    fault_ops = get_target_op(fault_model,fault_op_list)
    random.seed(datatime.now())
    op = random.choise(fault_ops)
    instance = get_target_op(op,file_op)
    write_to_fuse(flag,fault_model,op,instance)
    if fault_model == 'bitflip':
        specs = get_bitflip_spec(fault_model_spec_loader)
        write_fault_model_spec(fault_model,specs)
    if fault_model == 'shornwrite':
        specs = get_shornwrite_spec(fault_model_spec_loader)
        write_fault_model_spec(fault_model,specs)
    


