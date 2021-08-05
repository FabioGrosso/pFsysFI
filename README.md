# pFsysFI


This is the repo for file system fault injector. The idea is to help application developers to understand how the application would react to the failure of the underline file system. For example, Lustre offers fail-over mode for applications to survive the failure. The fault injector would inject errors into the file system, which creates the senairo that makes the file system fall into the fail-over mode, and evaluate the impact on the application.

# How to run
requirement: libfuse(https://github.com/libfuse/libfuse/release)

After install the fuse, change the lib and include of fuse in the Makefile (normally, the include/ will be in your_dir/libfuse/include and the lib/ will be in the your_dir /libfuse/build/lib)

Then change the dir of CONFIG_FILE, CONFIG_BITFLIP_FILE and, CONFIG_SHORNWRITE_FILE in the fault.c to be your favorite place to run the fault injection, i.e., you_favor_dir/fifaaficonfig, you_favor_dir/ bitflip, and you_favor_dir/shornwrite.

Then go to you_favor_dir and mkdir fuse_dir (where the temp file would be) and mkdir root_dir (where the benchmark would be).

