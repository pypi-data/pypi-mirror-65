#!/bin/bash

DEST="${DEST:-/home/g/programmieren/python/dhe/dhe}"
PY_V="${PY_V:-36m}"

target="debug"

[[ "$1" == "--release" ]] && target="release"

PATH="/home/g/.cargo/bin/:$PATH" cargo build $@
cp target/${target}/libpy_dhe.so "${DEST}/py_dhe.cpython-${PY_V}-x86_64-linux-gnu.so"
