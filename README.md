# pFsysFI


This is the repo for file system fault injector. The idea is to help application developers to understand how the application would react to the failure of the underline file system. For example, Lustre offers fail-over mode for applications to survive the failure. The fault injector would inject errors into the file system, which creates the senairo that makes the file system fall into the fail-over mode, and evaluate the impact on the application.

# How to run
Requirement: libfuse(https://github.com/libfuse/libfuse/release)

After install the fuse, change the **lib** and **include** of fuse in the Makefile (normally, the include/ will be in your_dir/libfuse/include and the lib/ will be in the your_dir /libfuse/build/lib)
![image](https://user-images.githubusercontent.com/37393451/129422835-c1ce9014-0c8c-43bc-afc1-1700a96461e2.png)
Then change the dir of CONFIG_FILE, CONFIG_BITFLIP_FILE and, CONFIG_SHORNWRITE_FILE in the fault.c to be your favorite place to run the fault injection, i.e., **you_favor_dir**/fifaaficonfig, **you_favor_dir**/ bitflip, and **you_favor_dir**/shornwrite.
![image](https://user-images.githubusercontent.com/37393451/129422844-97d1653c-5cd8-427f-a29a-902585993b58.png)
Then you can try "make"
Then go to **you_favor_dir** and **$ mkdir fuse_dir** (where the temp file would be) and **$ mkdir root_dir** (where the benchmark would be).
We recommend that you copy the executable file generated in step x (**fifaaFS**) as well as **config.yaml** and **faultinject.py** into **you_favor_dir**
![image](https://user-images.githubusercontent.com/37393451/129422863-f4d8ddbe-c1ce-4f91-afa6-dbaa5b051773.png)

