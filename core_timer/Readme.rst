.. SPDX-License-Identifier: GPL-2.0-or-later

CoreTimer
=========

Setup
-----

Please setup a 2 core 4 thread virtual machine and install babeltrace2's python bindings. 

For Ubuntu 20.04 please use the babeltrace ppa which has both versions 1 and 2.

If you run this on a different cpu topology, please adjust the script's tests.

Please remember to apply my tracepoint patch to your custom kernel or adjust the script.

This tool requires you build a perf for your custom kernel with ctf support and install it. Example: copy it to /usr/local/bin/perf

You will need a root home directory + a traces folder in the root dir.

Run the deploy.sh script to copy analyize_trace to your /usr/local/bin dir.

Creating a trace
----------------

Enter root, do not run as sudo.

sudo su

Test script with sleep test (only run one time).

./take_trace.sh sleep_test

run the script

./take_trace.sh

Please see /root/traces for your trace.

Analyzing the trace
--------------------

Convert perf.data file into a ctf trace inside a directory named ctf:

perf data convert --to-ctf=./ctf

Run the script:

analyze_trace ctf