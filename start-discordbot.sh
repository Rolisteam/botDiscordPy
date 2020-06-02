#!/bin/bash

export DISPLAY=:1
cd /home/renaud/application/mine/discord-python/

RunInstance() {
    while [ 1 ]
    do
        ./diceparser.py --shardCount $1 $2
        sleep 5m
    done
}


total=1

RunInstance $total 0 &




let lastId=total-1
#for i in `seq 0 $lastId`
#do
#	RunInstance $total i &
#done
