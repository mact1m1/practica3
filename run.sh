#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export PYTHONPATH="$root/src"
exec "${PYTHON:-python3}" -m uvm "$@"
