.. SPDX-License-Identifier: GPL-2.0-or-later

CoreTimer
=========

Setup
-----

Please setup a 2 core 4 thread virtual machine and install babeltrace2's python bindings. Currently the trace script only supports 4 threads.

For Ubuntu 20.04 please use the babeltrace ppa which has an up to date version of babeltrace2.

If you run this on a different cpu topology, please adjust the script's tests.

Please remember to apply my tracepoint patch to your custom kernel or adjust the script that is in the core_timer directory.

This tool requires you build a perf for your custom kernel with ctf support and install it to the system path. Example: copy it to /usr/local/bin/perf

Set up
----------------

Run the deploy script in the core_timer folder:

./deploy.sh

This copies two commands to your path.

Creating a trace
----------------

Create a folder to hold the individual test data.

Enter root, do not run the trace script as sudo.

sudo su

Test script with sleep test (only run one time).

take_trace sleep_test

run the script

take_trace

There should be a perf.data and a folder called ctf.

Analyzing the trace
--------------------

Run the script:

analyze_trace ctf