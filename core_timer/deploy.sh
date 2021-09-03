#!/usr/bin/env bash

sudo cp analyze_trace.py /usr/local/bin/analyze_trace

if [ $# -ge 1 ]; then
	if [ "$1" == "-a" ]; then
		sudo su -c "cd /root/traces && analyze_trace /root/traces/perf-all/ctf-all"
	fi
fi