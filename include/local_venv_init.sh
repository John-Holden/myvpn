#!/bin/bash

## Configure local pip venv from requirements file ##

RED='\033[0;31m'
NC='\033[0m' # No Color

printf "${NC}[i] Configuring local venv...\n"

if [ "$#" -gt 1 ]; then
    printf "${RED} [E] Illegal number of parameters - expected either none or requirements file location!"
    exit 1
elif [ "${#}" == 1 ]; then
    REQUIREMENTS="${1}"
else
    REQUIREMENTS="requirements.txt"
fi

if [ ! -d venv ]; then
    printf "${NC}[i] No venv detected, creating...\n"
    virtualenv venv
else
    printf "${NC}[i] Existing venv detected\n"
fi

if [ -f "${REQUIREMENTS}" ]; then
    printf "${NC}[i] pip installing from ${REQUIREMENTS}...\n"
    . ./venv/bin/activate
    pip3 install -q -r ${REQUIREMENTS}
    printf "${NC}[i] Done\n"
    exit 0
fi

printf "${RED} [E] Could Not find requirements file: ${REQUIREMENTS}..."
exit 1

