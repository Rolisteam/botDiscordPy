#!/usr/bin/python3.5

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

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

secs=3600*24
filename="alias.json"
description = '''DiceParser provides a complete system to run dice commands.'''
my_bot = Bot(command_prefix='',description=description)

msgCounter=100
channels = {}

messages = ["Hello, this bot is part of Rolisteam project. To ensure long-term viability please support us: https://liberapay.com/Rolisteam/donate",
                "Documentation is available here: https://github.com/Rolisteam/DiceParser/blob/master/HelpMe.md",
                "Rolisteam is a free virtual tabletop software dedicated to role playing games. You already know how to roll dice :-) http://www.rolisteam.org",
                "Need new features ? Ask them here: https://github.com/Rolisteam/DiceParser/issues"]


## INIT
AllAliases={}


if  os.path.exists(filename):
    with open(filename, 'r') as f:
        try:
            AllAliases = json.load(f)
        except:
            pass



async def manageAlias(message):
    idServer=str(message.server.id)
    aliases={}
    commands=[]
    aliasName=""
    addAlias=False
    removeAlias=False
    firstLine=True
    for line in message.content.splitlines():
        tab=line.split(' ')
        if(not addAlias and not removeAlias and firstLine):
            if(tab[0] == "!alias"):
                if(tab[1] == "rm"):
                    removeAlias=True
                    aliasName=tab[2]
                else:
                    addAlias=True
                    aliasName=tab[1]
        if(addAlias):
            if(firstLine):
                cmd=""
                for i in range(2,len(tab)):
                    if(i!=tab[0]):
                        cmd+=str(tab[i])+" "
                if(len(cmd)>0):
                    commands.append(cmd)
            else:
                commands.append(line)
        firstLine=False

    if( idServer not in AllAliases):
        AllAliases.update({str(idServer):{}})

    val = AllAliases[idServer]
    if(addAlias):
        val.update({str(aliasName):commands})   
    elif(removeAlias):
        del val[aliasName]
    
    with open(filename, 'w') as outfile:
        json.dump(AllAliases,outfile,indent=4)


@my_bot.event
async def rollDice(command,message,bot):
    logger = logging.getLogger('discord')
    kill = lambda process: process.kill()
    cmd = ['dice','-m',command]
    roll = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    my_timer = Timer(5, kill, [roll])
    try:
        my_timer.start()
        stdout, stderr = roll.communicate()
        logger.info("Result: "+stdout)
        await bot.send_message(message.channel, stdout)
        if (message.channel.id in channels):
            channels[message.channel.id] += 1
            if(channels[message.channel.id] == 1000):
                index = random.randint(0,len(messages)-1)
                ads = messages[index]
                logger.info("Ads:"+ads+" channel:"+message.channel.name)
                await bot.send_message(message.channel, ads)
                channels[message.channel.id] = 0
        else :
            channels[message.channel.id] = 0
    except:
        pass
        await my_bot.send_message(message.channel, "Error: your command took too much time")
    finally:
        my_timer.cancel()

## Callback
@my_bot.event
async def on_ready():
    print('Logged in as')
    print(my_bot.user.name)
    print(my_bot.user.id)
    print('------')
    logger.info("#### Server count: "+str(len(list(my_bot.servers))))
    #t.start()

@my_bot.event
async def on_read():
    print("Client logged in")

@my_bot.event
async def on_message(message):
    logger = logging.getLogger('discord')
    idServer=""
    if(message.server is not None):
        idServer = str(message.server.id)
    if message.content.startswith('!') and message.author != my_bot.user:
        if message.content.startswith('!play') or message.content.startswith('!skip'):
                    return
        if message.content.startswith('!alias'):
            await manageAlias(message)
        else:
            command = message.content[1:]
            normalCmd=True
            if(len(idServer) >0 and idServer in AllAliases):
                val = AllAliases[idServer]
                if(command in val):
                    cmds=val[command]
                    for line in cmds:
                        if(line.startswith('!')):
                            line = line[1:]
                        logger.info("Command: "+line)
                        normalCmd=False
                        await rollDice(line,message,my_bot)
            if(normalCmd):
                logger.info("Command: "+command)                
                await rollDice(command,message,my_bot)

#t = perpetualTimer(secs, sendOffAds)

#Prod
my_bot.run("Mjc5NzIyMzY5MjYwNDUzODg4.DBMyFg.V3syHisZumUGxyf5u5giQb6NYdk")

#Debug 
#my_bot.run("MzkxMzAxNDU2MjMxMTM3Mjky.DRWrew.1LjVb2w702Mtu9fURpU64yGlTyM")
#t.cancel()
