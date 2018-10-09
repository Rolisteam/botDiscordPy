#!/bin/bash

export DISPLAY=:1
cd /home/renaud/application/mine/discord-python/

RunInstance() {
    while [ 1 ]
    do
        ./diceparser.py --shardCount $1 $2
    done
}


total=4

RunInstance $total 0 &
RunInstance $total 1 &
RunInstance $total 2 &
RunInstance $total 3 &




#while [ 1 ]
#do
#	./diceparser.py --shardCount 3 0 &
#    ./diceparser.py --shardCount 3 1 &
#    ./diceparser.py --shardCount 3 2
#done
