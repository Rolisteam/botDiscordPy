import dbl
import discord
from discord.ext import commands

import aiohttp
import asyncio
import logging


class DiscordBotsOrgAPI(commands.Cog):
    """Handles interactions with the discordbots.org API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjI3OTcyMjM2OTI2MDQ1Mzg4OCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTMyMzg4NjU2fQ.qFDHEUhZbe3WMWHc-Uj3wWUIupm192AdJbWcC3IXC44'  #  set this to your DBL token
        self.dblpy = dbl.Client(self.bot, self.token, autopost=True)
        self.bot.loop.create_task(self.update_stats())

    async def on_guild_post():
        print("Server count posted successfully")


def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(DiscordBotsOrgAPI(bot))
