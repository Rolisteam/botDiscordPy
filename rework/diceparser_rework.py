#!/usr/bin/python3

import discord
import subprocess
from discord.ext.commands import Bot
from subprocess import run,Popen, PIPE
import logging
from threading import Timer,Thread,Event
import random
from datetime import datetime
import json
import os
import base64
import io
import argparse
import sys
import os.path
import dbl
from discord.ext import commands
from cogs import api
import aiohttp
import asyncio
import logging
import getopt
from dicebot import DiceBot

msgCounter=100
channels = {}

messages = ["Hello, this bot is part of Rolisteam project. To ensure long-term viability please support us: https://liberapay.com/Rolisteam/donate",
                "Documentation is available here: https://github.com/Rolisteam/DiceParser/blob/master/HelpMe.md",
                "Rolisteam is a free virtual tabletop software dedicated to role playing games. You already know how to roll dice :-) http://www.rolisteam.org",
                "Need new features ? Ask them here: https://github.com/Rolisteam/DiceParser/issues"]


def readAliases(aliasFile):
    if os.path.exists(aliasFile):
        with open(aliasFile, 'r') as f:
            try:
                return json.load(f)
            except:
                pass

def readPrefixes(prefixFile):
    if os.path.exists(prefixFile):
        with open(prefixFile, 'r') as fp:
            try:
                return json.load(fp)
            except:
                pass

def readMacro(dirname):
    AllMacro={}
    for fileMacro in os.listdir(dirname):
        idJson = fileMacro[6:-5]
        AllMacro[idJson]=fileMacro
    return AllMacro

#my_bot.run("Mjc5NzIyMzY5MjYwNDUzODg4.DzBGCA.QjJAGewTZr7eVovN18Gxvu2QnAM")
def Usage():
    print("Usage")
    print("")
    print("-h, --help")
    print("-s, --shardCount number; 1, 2, .. 10")

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hs:",["help","shardCount"])
    except getopt.GetoptError:
        Usage()
        sys.exit(2)

    shardCount = 0
    filename="alias.json"
    macroFileName="/home/renaud/application/mine/discord-python/macros/"
    description = '''DiceParser provides a complete system to run dice commands.'''
    prefixFile="prefix.json"

    alias=readAliases(filename)
    macros=readMacro(macroFileName)
    prefixes=readPrefixes(prefixFile)

    for key,value in opts:
        if( key == '-h'):
            Usage()
            sys.exit(0)
        elif (key in ('-s','--shardCount')):
            shardCount=value

    shards = []
    for i in range(int(shardCount)):
        bot = DiceBot(i,shardCount, alias, macros, prefixes)
        shards.insert(i,bot)
        print("start bot"+str(i))
        bot.start()

    for x in shards:
        x.join()

if __name__ == "__main__":
    main(sys.argv[1:])
