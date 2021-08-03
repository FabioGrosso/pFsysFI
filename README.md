# pFsysFI


This is the repo for file system fault injector. The idea is to help application developers to understand how the application would react to the failure of the underline file system. For example, Lustre offers fail-over mode for applications to survive the failure. The fault injector would inject errors into the file system, which creates the senairo that makes the file system fall into the fail-over mode, and evaluate the impact on the application.

# How to run
requirement: libfuse(https://github.com/libfuse/libfuse)

