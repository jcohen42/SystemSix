#!/bin/bash
cd $(dirname $0)
sleep 10s
feh -FYZ --force-aliasing --auto-reload INK_EXPORT.bmp &
python3 ./systemsix.py
wait