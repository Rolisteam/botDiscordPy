#!/bin/bash

export DISPLAY=:1
cd /home/renaud/application/mine/discord-python/

RunInstance() {
    while [ 1 ]
    do
        ./diceparser.py --shardCount $1 $2
    done
}


total=15

RunInstance $total 0 &
RunInstance $total 1 &
RunInstance $total 2 &
RunInstance $total 3 &
RunInstance $total 4 &
RunInstance $total 5 &
RunInstance $total 6 &
RunInstance $total 7 &
RunInstance $total 8 &
RunInstance $total 9 &
RunInstance $total 10 &
RunInstance $total 11 &
RunInstance $total 12 &
RunInstance $total 13 &
RunInstance $total 14 &




let lastId=total-1
#for i in `seq 0 $lastId`
#do
#	RunInstance $total i &
#done
