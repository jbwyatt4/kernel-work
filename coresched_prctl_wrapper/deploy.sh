#!/usr/bin/env bash

set -e

gcc -g main.c -o prctl_wrapper

./prctl_wrapper

./prctl_wrapper "stress-ng"

sudo cp prctl_wrapper /usr/local/bin/prctl_wrapper
