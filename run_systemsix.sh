#!/bin/bash
cd $(dirname $0)
feh -FYZ --force-aliasing --auto-reload INK_EXPORT.bmp &
source venv/bin/activate
python3 ./systemsix.py
wait