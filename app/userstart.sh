#!/bin/bash
#
# Deep Learning Studio - GUI platform for designing Deep Learning AI without programming
#
# Copyright (C) 2016-2017 Deep Cognition Labs, Skiva Technologies Inc.
#
# All rights reserved.
#
export PYTHONPATH=/home/app
export HOME=/home/app
export LD_LIBRARY_PATH="/usr/local/nvidia/lib:/usr/local/nvidia/lib64:"

if [ ! -d "/data/$USERID/deploy" ]; then
	mkdir -p /data/$USERID/deploy
fi

export DEPLOY_DIR=/data/$USERID/deploy

if [ -d "/usr/local/nvidia/bin" ]; then
  echo ********Detected CUDA path********
  export PATH="/usr/local/nvidia/bin:/usr/local/cuda/bin:$PATH"
fi
if [ -f app.so ]; then
  ./app.so &
else
  python app.py  &
fi

olympus up --no-debug --port 6666 --host 127.0.0.1 &