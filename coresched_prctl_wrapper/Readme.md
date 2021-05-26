
# Coresched prctl Wrapper

At the time, the Linux kernel only allowed a prctl interface to set a process to use coresched's core grouping features. An easy way to test this was with a C wrapper that calls the executing program.

To compile and run on a coresched kernel:
./run.sh