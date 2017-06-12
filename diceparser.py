#!/usr/bin/python3.5

import discord
import subprocess
from discord.ext.commands import Bot
from subprocess import run,Popen, PIPE
import logging


logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

description = '''DiceParser provides a complete system to run dice commands.'''
my_bot = Bot(command_prefix='',description=description)


@my_bot.event
async def on_ready():
    print('Logged in as')
    print(my_bot.user.name)
    print(my_bot.user.id)
    print('------')

@my_bot.event
async def on_read():
    print("Client logged in")


@my_bot.event
async def on_message(message):
    if message.content.startswith('!') and message.author != my_bot.user:
        command = message.content[1:]
        print(command)
        kill = lambda process: process.kill()
        cmd = ['dice','-m',command]
        roll = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
         
        my_timer = Timer(5, kill, [ping])
         
        try:
            my_timer.start()
            stdout, stderr = ping.communicate()
        finally:
            my_timer.cancel()
        result = subprocess.run(['timeout', '5','dice','-m',command],stdout=PIPE, stderr=PIPE, universal_newlines=True)
        print(result.stdout, result.returncode)
        await my_bot.send_message(message.channel, result.stdout)

#@my_bot.command()
#async def hello(*args):









#    return await my_bot.say("Hello, world!")

my_bot.run("Mjc5NzIyMzY5MjYwNDUzODg4.DBMyFg.V3syHisZumUGxyf5u5giQb6NYdk")
