# pFsysFI


This is the repo for file system fault injector. The idea is to help application developers to understand how the application would react to the failure of the underline file system. For example, Lustre offers fail-over mode for applications to survive the failure. The fault injector would inject errors into the file system, which creates the senairo that makes the file system fall into the fail-over mode, and evaluate the impact on the application.

# How to run
Requirement: libfuse(https://github.com/libfuse/libfuse/release), Ubuntu

1. After install the fuse, change the **INCLUDES** and **LFLAGS** of fuse in the Makefile (normally, the include/ will be in your_dir/libfuse/include and the lib/ will be in the your_dir /libfuse/build/lib)

![image](https://user-images.githubusercontent.com/37393451/129422835-c1ce9014-0c8c-43bc-afc1-1700a96461e2.png)

2. Then change the dir of CONFIG_FILE, CONFIG_BITFLIP_FILE and, CONFIG_SHORNWRITE_FILE in the fault.c to be your favorite place to run the fault injection, i.e., **you_favor_dir**/fifaaficonfig, **you_favor_dir**/ bitflip, and **you_favor_dir**/shornwrite.

![image](https://user-images.githubusercontent.com/37393451/129422844-97d1653c-5cd8-427f-a29a-902585993b58.png)

3. You can try **$ make** now, and a executable named **fifaaFS** will appear

4. Then go to **you_favor_dir** and **$ mkdir fuse_dir** (where the temp file would be) and **$ mkdir root_dir** (where the benchmark would be).

5. We recommend that you copy the executable file generated in step 3 (**fifaaFS**) as well as **config.yaml** and **faultinject.py** into **you_favor_dir**

![image](https://user-images.githubusercontent.com/37393451/129422863-f4d8ddbe-c1ce-4f91-afa6-dbaa5b051773.png)

6. Put the benchmark in **root_dir** and make sure that the file generate by benchmark would be place in to **fuse_dir**

![image](https://user-images.githubusercontent.com/37393451/129429435-3bbb801b-0944-4faa-b8f6-2d04f10012cc.png)

7. Then go to the config.yaml and change the parameter under fuse accordingly 

![image](https://user-images.githubusercontent.com/37393451/129429441-4475a3f9-eadc-4fda-83ae-0040e0c2bf6b.png)

You will also need to change the **benchmark** and **parameters** 

![image](https://user-images.githubusercontent.com/37393451/129429455-07eb25f4-a2a3-4a2c-93d7-8e4eeddf85db.png)

And change the written_file to where the file would be written to as well as change the log_file

![image](https://user-images.githubusercontent.com/37393451/129429474-abbbe48b-54aa-43c4-a84a-46ac93c075b6.png)

8. After that you can try “python3 faultinject.py” and the result will be in you_favor_dir

![image](https://user-images.githubusercontent.com/37393451/129429481-5130c7c6-adbf-4932-aac6-606be50e7de1.png)


