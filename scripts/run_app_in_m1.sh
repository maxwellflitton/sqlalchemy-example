#!/usr/bin/env bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
cd $SCRIPTPATH
cd ..
source venv/bin/activate
cd src

export PYTHONPATH="$PWD"
arch -x86_64 /bin/bash -c "python app.py"
