#!/bin/bash

if [ ! -d venv ]; then
    echo "[i] No venv detected, creating..."
    virtualenv venv
else
    echo "[i] Venv detected"
fi

. ./venv/bin/activate
pip3 install -q -r  requirements.txt

