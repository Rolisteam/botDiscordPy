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

import aiohttp
import asyncio
import logging

parser = argparse.ArgumentParser()
parser.add_argument("shard_id", help="current proccess shard_id",type=int)
parser.add_argument("-c","--shardCount", help="max shard", type=int)
args = parser.parse_args()

current_shard_id=args.shard_id
shardCount = args.shardCount
#shardCount= 3

print(str(current_shard_id)+" "+str(shardCount));
#sys.exit(0)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

secs=3600*24
filename="alias.json"
macroFileName="/home/renaud/application/mine/discord-python/macros/"
description = '''DiceParser provides a complete system to run dice commands.'''
prefixFile="prefix.json"
my_bot = Bot(shard_id=current_shard_id,shard_count=shardCount,command_prefix='')
#(command_prefix='',description=description,shard_id=0,shard_count=1)

msgCounter=100
channels = {}

messages = ["Hello, this bot is part of Rolisteam project. To ensure long-term viability please support us: https://liberapay.com/Rolisteam/donate",
                "Documentation is available here: https://github.com/Rolisteam/DiceParser/blob/master/HelpMe.md",
                "Rolisteam is a free virtual tabletop software dedicated to role playing games. You already know how to roll dice :-) http://www.rolisteam.org",
                "Need new features ? Ask them here: https://github.com/Rolisteam/DiceParser/issues"]


## INIT
AllAliases={}
AllMacro={}
PrefixByServer={}



if  os.path.exists(filename):
    with open(filename, 'r') as f:
        try:
            AllAliases = json.load(f)
        except:
            pass
    with open(prefixFile, 'r') as fp:
        try:
            PrefixByServer = json.load(fp)
        except:
            pass
    for fileMacro in os.listdir(macroFileName):
        idJson = fileMacro[6:-5]
        print(idJson)
        AllMacro[idJson]=fileMacro



def getPrefix(serverId):
    if(serverId in PrefixByServer):
        return PrefixByServer[serverId]
    return "!"

async def managePrefix(idserver, textmsg, message, bot ):
    # !prefix set roll
    try:
        array=textmsg.split(' ')
        print(array)
        if(len(array)==3):
            if(array[0] == "prefix"):
                if(array[1] == "set"):
                    PrefixByServer[idserver]=array[2]


        with open(prefixFile, 'w') as outfile:
            json.dump(PrefixByServer,outfile,indent=4)
        await bot.send_message(message.channel, "[Prefix]New prefix definition is done!")
    except:
        await bot.send_message(message.channel, "[Prefix]Something goes wrong")


async def manageAdsMessage(message):
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

async def sendImageMessage(bot,message,data):
    decodedData=base64.b64decode(data,validate=True)
    f = io.BytesIO(decodedData)
    logger.info("data: "+data)
    await bot.send_file(message.channel, f, filename="result.png",content="")


async def manageMacro(message,bot):
    idServer=str(message.server.id)
    macroPattern=""
    macroCmd=""
    filename = "{}macro_{}.json".format(macroFileName,idServer)
    macros = []
    if os.path.isfile(filename):
        with open(filename) as f:
            macros = json.load(f)
    macroRegExp=False
    addMacro=False
    removeMacro=False
    showlistMacro = False
    idToRemove=-1

    for line in message.content.splitlines():
        tab=line.split(' ')
        if(not addMacro and not removeMacro):
            if(tab[0] == "!macro"):
                if(tab[1] == "rm"):
                    removeMacro=True
                    idToRemove=tab[2]
                elif(tab[1] == "list"):
                    showlistMacro=True
                else:
                    addMacro=True
                    macroName=tab[1]
                    try:
                        macroCmd = tab[2]
                    except IndexError:
                        await bot.send_message(message.channel, "Error in your add Macro Command: no command")

                    try:
                        macroRegExp=True if int(tab[3])==1 else False
                    except IndexError:
                        macroRegExp=False

    if(addMacro):
        macro = {}
        macro["pattern"]=macroName
        macro["cmd"]=macroCmd
        macro["regexp"]=macroRegExp
        macro["comment"]=""
        macros.append(macro)

    if(showlistMacro):
        lines=""
        id = 0
        for i in macros:
            lines+="id: {} Pattern: {} Command: {} Regexp: {}\n".format(id,i["pattern"],i["cmd"],i["regexp"])
            id+=1
        if(id>0):
            await bot.send_message(message.channel, lines)

    if(removeMacro):
        try:
            del macros[int(idToRemove)]
        except IndexError:
            await bot.send_message(message.channel, "Error in your remove Macro Command")


    if(removeMacro or addMacro):
        with open(filename, 'w') as outfile:
            json.dump(macros,outfile,indent=4)
            AllMacro[idServer]="macro_{}.json".format(idServer)


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
                    try:
                        aliasName=tab[2]
                    except IndexError:
                        print("error index in alias")
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


async def rollDice(command,message,bot):
    idServer=str(message.server.id)
    logger = logging.getLogger('discord')
    kill = lambda process: process.kill()
    cmd = ['dice','-b',command]
    if idServer in AllMacro:
        cmd.append('-a');
        cmd.append("{}{}".format(macroFileName,AllMacro[idServer]));
    roll = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    my_timer = Timer(5, roll.kill)
    try:
        my_timer.start()
        stdout, stderr = roll.communicate()
        print(stdout)
        print(stderr)
        rc = roll.returncode
        if (rc == 0):
            logger.info("command: "+command+" Result: "+stdout)
            if(stdout.endswith("```")):
                await bot.send_message(message.channel, stdout)
            else:
                await sendImageMessage(bot,message,stdout)
            await manageAdsMessage(message)
    except OSError as inst:
        logger.info(type(inst))    # the exception instance
        logger.info(inst)          # __str__ allows args to be printed directly,
        #await my_bot.send_message(message.channel, "Error: your command took too much time")
    except:
        logger.info("Unexpected error:"+str(sys.exc_info()[0]))
    finally:
        my_timer.cancel()

## Callback
@my_bot.event
async def on_ready():
    print('Logged in as')
    print(my_bot.user.name)
    print(my_bot.user.id)
    print('------')
    logger.info("#### Server count (shard "+str(current_shard_id)+"): "+str(len(list(my_bot.servers)))+" serverCount:"+str(len(self.bot.guilds)))
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
        prefix = getPrefix(idServer)
        textmsg = message.content
        if textmsg.startswith(prefix) and message.author != my_bot.user:
            textmsg= textmsg[len(prefix):].strip()
            if textmsg.startswith('play') or textmsg.startswith('skip'):
                        return
            if textmsg.startswith('alias'):
                await manageAlias(message)
            if textmsg.startswith('macro'):
                await manageMacro(message,my_bot)
            if textmsg.startswith('prefix'):
                logger.info("Confix prefix")
                await managePrefix(idServer,textmsg,message,my_bot)
            else:
                command = textmsg
                normalCmd=True
                if(len(idServer) >0 and idServer in AllAliases):
                    val = AllAliases[idServer]
                    if(command in val):
                        cmds=val[command]
                        for line in cmds:
                            if(line.startswith('!')):
                                line = line[1:]
                            logger.info("Saved Command: "+line)
                            normalCmd=False
                            await rollDice(line,message,my_bot)
                if(normalCmd):
                    await rollDice(command,message,my_bot)


#Prod
my_bot.run("Mjc5NzIyMzY5MjYwNDUzODg4.DcBL0A.UMEDCkhqka8GIgZOb_GnvhSJ_rc")

#Debug
#my_bot.run("MzkxMzAxNDU2MjMxMTM3Mjky.DRWrew.1LjVb2w702Mtu9fURpU64yGlTyM")
