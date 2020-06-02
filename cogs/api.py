import dbl
import discord
from discord.ext import commands

import aiohttp
import asyncio
import logging


class DiscordBotsOrgAPI(commands.Cog):
    """Handles interactions with the discordbots.org API"""

    def __init__(self, bot, shardId, shardCount):
        self.bot = bot
        self.shardId = shardId
        self.shardCount = shardCount
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjI3OTcyMjM2OTI2MDQ1Mzg4OCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTMyMzg4NjU2fQ.qFDHEUhZbe3WMWHc-Uj3wWUIupm192AdJbWcC3IXC44'  #  set this to your DBL token
        self.dblpy = dbl.Client(self.bot, self.token)
        self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""

        while True:
            logger.info('attempting to post server count')
            try:
                await self.dblpy.post_server_count(self.shardCount, self.shardId)
                #logger.info('posted server count ({})'.format(self.bot.guilds()))
                #logger.info('shardCount:{} shardId: {}'.format(self.shardCount,self.shardId))
            except Exception as e:
                logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
            await asyncio.sleep(1800)


def setup(bot, shardId, shardCount):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(DiscordBotsOrgAPI(bot))
