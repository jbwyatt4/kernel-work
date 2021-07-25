#!/usr/bin/env bash

set -e

gcc -g main.c

./a.out

./a.out "stress-ng"

sudo cp a.out /usr/local/bin/prctl_wrapper
