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


total=35

RunInstance $total 0 &
sleep 2s
RunInstance $total 1 &
sleep 2s
RunInstance $total 2 &
sleep 2s
RunInstance $total 3 &
sleep 2s
RunInstance $total 4 &
sleep 2s
RunInstance $total 5 &
sleep 2s
RunInstance $total 6 &
sleep 2s
RunInstance $total 7 &
sleep 2s
RunInstance $total 8 &
sleep 2s
RunInstance $total 9 &
sleep 2s
RunInstance $total 10 &
sleep 2s
RunInstance $total 11 &
sleep 2s
RunInstance $total 12 &
sleep 2s
RunInstance $total 13 &
sleep 2s
RunInstance $total 14 &
sleep 2s
RunInstance $total 15 &
sleep 2s
RunInstance $total 16 &
sleep 2s
RunInstance $total 17 &
sleep 2s
RunInstance $total 18 &
sleep 2s
RunInstance $total 19 &
sleep 2s
RunInstance $total 20 &
sleep 2s
RunInstance $total 21 &
sleep 2s
RunInstance $total 22 &
sleep 2s
RunInstance $total 23 &
sleep 2s
RunInstance $total 24 &
sleep 2s
RunInstance $total 25 &
sleep 2s
RunInstance $total 26 &
sleep 2s
RunInstance $total 27 &
sleep 2s
RunInstance $total 28 &
sleep 2s
RunInstance $total 29 &
sleep 2s
RunInstance $total 30 &
sleep 2s
RunInstance $total 31 &
sleep 2s
RunInstance $total 32 &
sleep 2s
RunInstance $total 33 &
sleep 2s
RunInstance $total 34 &



let lastId=total-1
#for i in `seq 0 $lastId`
#do
#	RunInstance $total i &
#done
