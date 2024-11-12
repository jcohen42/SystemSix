#!/bin/bash
cd $(dirname $0)
eog --fullscreen INK_EXPORT.bmp
python3 ./systemsix.py