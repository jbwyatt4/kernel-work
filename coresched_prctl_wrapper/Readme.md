
# Coresched prctl Wrapper

At the time, the Linux kernel only allows a prctl interface to set a process to use coresched's core grouping features.

An easy way to test this was with a C wrapper that calls the executing program.

To compile and test on a coresched kernel, run:

./deploy.sh

This will copy the wrapper to /usr/local/bin

so you can use

prctl_wrapper in the future