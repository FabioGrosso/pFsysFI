import os
import shutil
import sys
import re
import yaml
import subprocess
import random
from datetime import datetime
import time

# get the benchmark xml for the profiling data
YAML = ".yaml"
CONFIG = "config"
FS_PREFIX = "fifaa"
OP_MATCHING = FS_PREFIX+"_"+r'.*\(.*?\)'
FS_LOG = FS_PREFIX+".log"
ERROR_FILE = "_ficonfig"
FUSECOMMAND = "fusermount3"


def config_loader(configfile:str):
    yaml_file = open(configfile)
    if yaml_file.closed:
        print("file is not open")
        raise ValueError

    parsed_yaml_loader = yaml.load(yaml_file, Loader=yaml.FullLoader)
    return parsed_yaml_loader

def parse_log(logfile:str,yaml_loader) -> dict:

    file_op = {}
    with open(logfile) as f:
        lines = f.readlines()
        for line in lines:
            if FS_PREFIX in line:
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
        print("file is not open")
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

def get_faultmodel_op(fault_model,fault_op_loader)->list:
    
    if fault_model == "bitflip":
        if "bitflip" not in fault_op_loader:
            print("bitflip fault op not configured")
            raise ValueError
        return fault_op_loader['bitflip']

    if fault_model == "shornwrite":
        if "shornwrite" not in fault_op_loader:
            print("shornwrite fault op not configured")
            raise ValueError
        return fault_op_loader['shornwrite']

def get_target_op(op,file_op)->int:

    total = file_op[op]
    random.seed(datetime.now())
    return random.randint(0,total-1)


def get_inject_model(yaml_loader):

    if 'injection' not in yaml_loader:
        print("injection section not configured")
        raise ValueError
    return yaml_loader['injection']

def get_fault_op(yaml_loader):

    if 'fault_op' not in yaml_loader:
        print("fault op section not configured")
        raise ValueError
    return yaml_loader['fault_op']

def get_fuse_config(yaml_loader):

    if 'fuse' not in yaml_loader:
        print("fault op section not configured")
        raise ValueError
    return yaml_loader['fuse']

def get_fuse_mountpoint(fuse_loader):
    if 'mount' not in fuse_loader:
        print("fuse mount point not configured")
        raise ValueError
    return fuse_loader['mount']

def get_fuse_root(fuse_loader):
    if 'root' not in fuse_loader:
        print("root not configured")
        raise ValueError
    return fuse_loader['root']

def get_fuse_execute(fuse_loader):
    if 'fuseFS' not in fuse_loader:
        print("fuseFS not configured")
        raise ValueError
    return fuse_loader['fuseFS']

def get_injection_flag(injection_loader)->int:

    if 'inject_flag' not in injection_loader:
        print("inject flag params not configured")
        raise ValueError
    return injection_loader['inject_flag']

def get_fault_model(injection_loader)->str:

    if 'fault_model' not in injection_loader:
        print("fault model params not configured")
        raise ValueError
    return injection_loader['fault_model']

def get_injection_trial(injection_loader)->int:

    if 'num_trials' not in injection_loader:
        print("num_trial params not configured")
        raise ValueError
    return injection_loader['num_trials']

def write_to_fuse(error_mode,fault_model,op_name,count):
        f = open(FS_PREFIX+ERROR_FILE,'w')
        f.write(str(error_mode))
        f.write("\n")
        f.write(str(fault_model))
        f.write("\n")
        f.write(str(op_name))
        f.write("\n")
        f.write(str(count))
        f.write("\n")
        f.close()

def get_app(yaml_loader)->str:
    if "benchmark" not in yaml_loader:
        print("benchmark not configured")
        raise ValueError
    return yaml_loader['benchmark']

def get_app_file(yaml_loader)->str:
    if "written_file" not in yaml_loader:
        print("written_file not configured")
        raise ValueError
    return yaml_loader['written_file']

def get_app_params(yaml_loader)->list:
    if "parameters" not in yaml_loader:
        print("benchmark not configured")
        raise ValueError

    return yaml_loader['parameters']

def get_fault_model_spec(yaml_loader):
    if "fault_model_spec" not in yaml_loader:
        print("benchmark not configured")
        raise ValueError
    return yaml_loader['fault_model_spec']

def get_bitflip_spec(fault_model_spec_loader):
    if "bitflip" not in fault_model_spec_loader:
        print("bitflip spec not configured")
        raise ValueError
    ret = []
    ret.append(fault_model_spec_loader['bitflip']['consecutive_bits'])
    return ret

def get_shornwrite_spec(fault_model_spec_loader):
    if "shornwrite" not in fault_model_spec_loader:
        print("shornwrite spec not configured")
        raise ValueError
    ret = []
    ret.append(fault_model_spec_loader['shornwrite']['shorn_portion'])
    return ret


def write_fault_model_spec(fault_model,specs):
    with open(fault_model,'w') as f:
        for spec in specs:
            f.write(str(spec))
            f.write("\n")

def run_command(params):
    process = subprocess.Popen(execution, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print("running command with the following message")
    stdout = stdout.decode("utf-8")
    stderr = stderr.decode("utf-8")
    print(stdout)
    print(stderr)
    return [stdout,stderr]

yaml_loader = config_loader(CONFIG+YAML)
app = get_app(yaml_loader)
params = get_app_params(yaml_loader)
app_file = get_app_file(yaml_loader)

fuse_loader = get_fuse_config(yaml_loader)

fuse_execute = get_fuse_execute(fuse_loader)

fuse_root = get_fuse_root(fuse_loader)

fuse_mount = get_fuse_mountpoint(fuse_loader)

#we assume there is no fuse mounted

execution = []
execution.append(fuse_execute)
execution.append(fuse_root)
execution.append(fuse_mount)
run_command(execution)
time.sleep(1)

# run profiling to get the fiffa log
execution = []
execution.append(app)
if params != None:
    execution.extend(params)
run_command(execution)

if os.path.isfile(FS_LOG) == False:
    print("NO FS LOG FILE FOUND")
    raise ValueError



execution = []

execution.append(FUSECOMMAND)
execution.append('-u')
execution.append(fuse_mount)
time.sleep(1)
# unmount the fuse
run_command(execution)

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

    fault_ops = get_faultmodel_op(fault_model,fault_op_list)
    random.seed(datetime.now())
    op = random.choice(fault_ops)
    instance = get_target_op(op,file_op)
    write_to_fuse(flag,fault_model,op,instance)
    if fault_model == 'bitflip':
        specs = get_bitflip_spec(fault_model_spec_loader)
        write_fault_model_spec(fault_model,specs)
    if fault_model == 'shornwrite':
        specs = get_shornwrite_spec(fault_model_spec_loader)
        write_fault_model_spec(fault_model,specs)
    # launch fuse
    execution = []
    execution.append(fuse_execute)
    execution.append(fuse_root)
    execution.append(fuse_mount)
    run_command(execution)
    time.sleep(1)
    # run app
    execution = []
    execution.append(app)
    if params != None:
        execution.extend(params)
    [stdout,stderr] = run_command(execution)
    # post-process injection results
    os.mkdir(str(i))
    # save generted application result file /stdout to this directory, e.g
    path = os.path.join(str(i),"stdout")
    with open(path,"w") as f:
        f.write(stdout)
    path = os.path.join(str(i),"stderr")
    with open(path,"w") as f:
        f.write(stderr)
    shutil.copy2(app_file,str(i))    
    # unmount fuse
    execution = []
    execution.append(FUSECOMMAND)
    execution.append('-u')
    execution.append(fuse_mount)
    run_command(execution)
    time.sleep(1)


