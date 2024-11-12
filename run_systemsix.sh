#!/bin/bash
cd $(dirname $0)
sleep 10s
eog --fullscreen INK_EXPORT.bmp &
python3 ./systemsix.py
wait