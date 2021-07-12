#!/usr/bin/env bash

sudo cp analyze_trace.py /usr/local/bin/analyze_trace

if [ $# -ge 1 ]; then
	if [ "$1" == "-a" ]; then
		cd /root/traces
		analyze_trace ./ctf
	fi
fi