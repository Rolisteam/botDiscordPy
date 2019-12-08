#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
import configparser

import dbl
from discord.ext import commands
from cogs import api

import aiohttp
import asyncio
import logging

parser = argparse.ArgumentParser()
parser.add_argument("shard_id", help="current proccess shard_id",type=int)
parser.add_argument("-c","--shardCount", help="max shard", type=int)
args = parser.parse_args()
Testing=True
current_shard_id=args.shard_id
shardCount = args.shardCount
discordMsgLimit=2000
#shardCount= 3

print(str(current_shard_id)+" "+str(shardCount));
#sys.exit(0)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='/opt/document/log/discord.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

secs=3600*24
filename="alias.json"
macroFileName="/home/renaud/application/mine/discord-python/macros/"
pwd="/home/renaud/application/mine/discord-python/"
description = '''DiceParser provides a complete system to run dice commands.'''
prefixFile="prefix.json"
client = discord.AutoShardedClient(shard_count=shardCount)
#(command_prefix='',description=description,shard_id=0,shard_count=1)

msgCounter=100
channels = {}

messages = ["Hello, this bot is part of Rolisteam project. To ensure long-term viability please support us: https://liberapay.com/Rolisteam/donate",
                "Documentation is available here: https://github.com/Rolisteam/DiceParser/blob/master/HelpMe.md",
                "Rolisteam is a free virtual tabletop software dedicated to role playing games. You already know how to roll dice :-) http://www.rolisteam.org",
                "Need new features ? Ask them here: https://github.com/Rolisteam/DiceParser/issues"]


## INIT
config = configparser.ConfigParser()
config.read(pwd+"config.conf")
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
        await message.channel.send( "[Prefix]New prefix definition is done!")
    except:
        await message.channel.send( "[Prefix]Something goes wrong")


async def manageAdsMessage(message):
    if (message.channel.id in channels):
        channels[message.channel.id] += 1
        if(channels[message.channel.id] == 1000):
            index = random.randint(0,len(messages)-1)
            ads = messages[index]
            logger.info("Ads:"+ads+" channel:"+message.channel.name)
            await message.channel.send(ads)
            channels[message.channel.id] = 0
    else :
        channels[message.channel.id] = 0

async def sendImageMessage(bot,message,data):
    decodedData=base64.b64decode(data,validate=True)
    f = io.BytesIO(decodedData)
    logger.info("data: "+data)
    await message.channel.send( f, file="result.png",content="")


async def manageMacro(message,textmsg,bot):
    global discordMsgLimit
    idServer=str(message.guild.id)
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

    tab=textmsg.split(' ')
    index=-1
    if(not addMacro and not removeMacro):
       if(tab[0] == "macro"):
           if(tab[1] == "rm"):
               removeMacro=True
               idToRemove=tab[2]
           elif(tab[1] == "list"):
               showlistMacro=True
           elif(tab[1][0] == ":"):
               strg=str(tab[1])
               print(strg)
               showlistMacro=True
               try:
                   index = int(strg[1:])
               except:
                   pass
           else:
               addMacro=True
               size=len(tab)
               macroName=tab[1]

               try:
                   macroRegExp=False
                   if(int(tab[size-1])==1):
                       macroRegExp=True
                       size-=1
                   elif(int(tab[size-1])==0):
                       size-=1
               except IndexError:
                    macroRegExp=False


               try:
                   macroCmd=""
                   for i in range(2, size):
                       macroCmd += " "+tab[i]
                       print("macro:"+macroCmd)
                   macroCmd=macroCmd.strip()
               except IndexError:
                   addMacro=False
                   await message.channel.send("Error in your add Macro Command: no command")


    if(addMacro):
        macro = {}
        macro["pattern"]=macroName
        macro["cmd"]=macroCmd
        macro["regexp"]=macroRegExp
        macro["comment"]=""
        macros.append(macro)
	if(count == 1):
            await message.channel.send("Macro has been added!")
        else:
            await message.channel.send("Faillure: Macro can't be added!")

    if(showlistMacro):
        lines="```"
        id = 0
        for i in macros:
            lines+="id: {} Pattern: {} Command: {} Regexp: {}\n\n".format(id,i["pattern"],i["cmd"],i["regexp"])
            id+=1
        lines+="```"
        if(id>0):
            if(len(lines)<discordMsgLimit):
                await message.channel.send(lines)
            else:
                await message.channel.send(lines[:2500])
        else:
            await message.channel.send("No recorded macro for this server")

    if(removeMacro):
        try:
            del macros[int(idToRemove)]
        except IndexError:
            await message.channel.send( "Error in your remove Macro Command")


    if(removeMacro or addMacro):
        with open(filename, 'w') as outfile:
            json.dump(macros,outfile,indent=4)
            AllMacro[idServer]="macro_{}.json".format(idServer)


async def manageAlias(message,textmsg,bot):
    idServer=str(message.guild.id)
    aliases={}
    commands=[]
    aliasName=""
    addAlias=False
    removeAlias=False
    showlistAlias=False
    firstLine=True
    for line in textmsg.splitlines():
        tab=line.split(' ')
        if(not addAlias and not removeAlias and firstLine):
            if(tab[0] == "alias"):
                if(tab[1] == "rm"):
                    removeAlias=True
                    try:
                        aliasName=tab[2]
                    except IndexError:
                        print("error index in alias")
                elif(tab[1] == "list"):
                    showlistAlias=True
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

    if(showlistAlias):
        val = AllAliases[idServer]
        lines="```"
        id = 0
        for i in val:
            if len(i) == 0:
                return
            cmds=val[i]
            print(cmds)

            lines+="id: {} Pattern: {}\nCommand:\n{}\n\n".format(id,i,"\n".join(cmds))
            id+=1
        lines+="```"
        if(id>0):
            await message.channel.send(lines)
        else:
            await message.channel.send("No recorded macro for this server")
        return

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
    idServer=str(message.guild.id)
    logger = logging.getLogger('discord')
    kill = lambda process: process.kill()
    cmd = ['xvfb-run','dice','-b',command]
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
            logger.info("cmd: "+str(command))
            if(stdout.endswith("```")):
                await message.channel.send(stdout)
            else:
                await sendImageMessage(bot,message,stdout)
            await manageAdsMessage(message)
        elif(rc != 1):
            logger.info("command FAIL: "+str(command)+" returncode:"+str(rc))
    except OSError as inst:
        logger.info(type(inst))    # the exception instance
        logger.info(inst)          # __str__ allows args to be printed directly,
        logger.info("OSError error: "+str(sys.exc_info()[0])+" cmd:"+str(command))
        #await client.send_message(message.channel, "Error: your command took too much time")
    except:
        msgError = sys.exc_info()
        logger.info("Unexpected error:"+str(msgError[0])+""+str(msgError[1])+""+str(msgError[2])+" cmd:"+str(command))
    finally:
        my_timer.cancel()

async def manageSupport(message, bot):
    await message.channel.send("You want to help ? Go to:\n https://liberapay.com/obiwankennedy/donate \nor\n https://www.patreon.com/rolisteam \nor\n https://www.twitch.tv/rolisteam to support my development")

async def manageVote(message, bot):
    await message.channel.send("Vote for Diceparser! go to: https://discordbots.org/bot/279722369260453888/vote")
## Callback
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print('id: {} count: {}'.format(current_shard_id,shardCount))
    game = discord.Game("!support !help !vote")
    await client.change_presence(status=discord.Status.idle, activity=game)
    if not Testing:
        api.setup(client)
    logger.info("#### Server count (shard "+str(current_shard_id)+"): "+str(len(list(client.guilds))))

@client.event
async def on_read():
    print("Client logged in")

@client.event
async def on_server_join(server):
    logger.info("#### Server count (shard "+str(current_shard_id)+"): "+str(len(list(client.guilds))))

@client.event
async def on_server_remove(server):
    logger.info("#### Server count (shard "+str(current_shard_id)+"): "+str(len(list(client.guilds))))


@client.event
async def on_message(message):
    logger = logging.getLogger('discord')
    idServer=""
    if(message.guild is not None):
        idServer = str(message.guild.id)
        prefix = getPrefix(idServer)
        textmsg = message.content
        if textmsg.startswith(prefix) and message.author != client.user:
            textmsg= textmsg[len(prefix):].strip()
            if textmsg.startswith('play') or textmsg.startswith('skip') or textmsg.startswith('stop'):
                        return
            elif textmsg.startswith('alias'):
                logger.info("alias")
                await manageAlias(message,textmsg,client)
            elif textmsg.startswith('macro'):
                logger.info("macro")
                await manageMacro(message,textmsg,client)
            elif textmsg.startswith('support'):
                logger.info("Support asked")
                await manageSupport(message, client)
            elif textmsg.startswith('vote'):
                logger.info("vote asked")
                await manageVote(message, client)
            elif textmsg.startswith('prefix'):
                logger.info("Confix prefix")
                await managePrefix(idServer,textmsg,message,client)
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
                            await rollDice(line,message,client)
                if(normalCmd):
                    await rollDice(command,message,client)


#Prod
if Testing:
    client.run(config['DEFAULT']['PKEY_DEV'])
else:
    client.run(config['DEFAULT']['PKEY'])

