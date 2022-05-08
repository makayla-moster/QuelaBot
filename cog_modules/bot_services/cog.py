import ast
import asyncio
import os
import traceback

import aiohttp
import disnake
from disnake.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()


class BotServices(commands.Cog):
    """A cog for bot service commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot Services cog has been loaded!")

    @commands.command(aliases=['quit', 'disconnect'])
    @commands.is_owner()
    async def logout(self, ctx):
        '''If the bot owner runs this command, then the bot disconnects.'''
        await ctx.send("Logging out!")
        await self.bot.close()

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     # if message.author.id == bot.id:
    #     #     return
    #
    #     if self.user.mention in message.content:
    #         await ctx.send("Hello!")


def setup(bot: commands.Bot):
    bot.add_cog(BotServices(bot))
