#!/usr/bin/env bash
source /home/kyfq/.virtualenvs/bms/bin/activate
cd /home/kyfq/MyPython/PycharmProjects/bms/services

# 先kill掉关于tiles_server的进程
pkill -f 'python -u crawl_server.py'
python -u crawl_server.py 5022 &
