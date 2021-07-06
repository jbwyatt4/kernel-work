#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-2.0-or-later

# Run with ./take_trace.sh
# will prompt for sudo in which it may fail the first time, run again
# ---
# Run with sudo bash -x take_trace.sh to debug script

if [[ $EUID -ne 0 ]]; then
	echo "Run me as root: sudo su and ./take_trace.sh"
	echo "Not sudo ./take_trace.sh; will get -g not found or other errors"
	exit 1
fi

set -e # Stop script on first error

mkdir -p /sys/fs/cgroup/cpu/test
cd /sys/fs/cgroup/cpu/test
echo 1 > cpu.core_tag
dmesg | grep "core sched" # ensure core sched message is running

if [ "$1" == "sleep_test" ]; then
	#warning: the sleep process must be at least 90 to be measured? [please find out why]
	cgexec -g cpu:test sleep 300 &
else
	cgexec -g cpu:test stress-ng --matrix 4 -t 2m &
fi

sleep 1s # Need to wait for the processes to be created
declare RESULT=($(cat cgroup.procs))

CONSTRUCT_TEXT=""
for i in "${RESULT[@]}"
do
	CONSTRUCT_TEXT="$CONSTRUCT_TEXT-p $i "
done
echo "A list of threads that are being measured should be below:"
echo $CONSTRUCT_TEXT
CTFSECONDS=`date +%s`
echo $CTFSECONDS > /root/traces/perf.meta
perf record -e 'irq:irq_handler_entry' -e 'sched:sched_switch' -e 'sched:sched_core_thread_cookie' -ag $CONSTRUCT_TEXT -o /root/traces/perf.data sleep 15
echo "AAA"
cd /root/traces/
perf data convert --to-ctf=./ctf