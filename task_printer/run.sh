#!/usr/bin/env bash

echo "requires kernel headers to be installed"

export MODULE_NAME="task_printer" ;

set -euo pipefail # Exit if any command returns nonzero

if [ $# -ge 1 ]; then
  if [ "$1" == "--clean" ]; then
    make clean
    exit 0
  fi

  if [ "$1" == "--reload" ]; then
    ./run.sh --clean
  fi
fi

make
sudo -v
make test
