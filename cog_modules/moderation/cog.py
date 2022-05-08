import ast
import asyncio
import os
import traceback

import aiohttp
import disnake
from disnake.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))


class Moderation(commands.Cog):
    """A cog for bot service commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded!")

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def kick(self, ctx, member: disnake.Member, *, reason=None):
        '''Moderators who call this command can kick members from the server.'''
        await ctx.guild.kick(user = member, reason = reason)

        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        message = disnake.Embed(
            title=f"{ctx.author.name} kicked: {member.name}",
            description= reason,
            color=disnake.Color.red(),
        )
        await channel.send(embed=message)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: disnake.Member, *, reason=None):
        '''Moderators who call this command can ban members from the server.'''
        await ctx.guild.ban(user = member, reason = reason)

        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        message = disnake.Embed(
            title=f"{ctx.author.name} banned: {member.name}",
            description= reason,
            color=disnake.Color.red(),
        )
        await channel.send(embed=message)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, member, *, reason=None):
        '''Moderators who call this command can unban members from the server.'''
        member = await self.bot.fetch_user(int(member))
        await ctx.guild.unban(member, reason = reason)

        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        message = disnake.Embed(
            title=f"{ctx.author.name} unbanned: {member.name}",
            description= reason,
            color=disnake.Color.red(),
        )
        await channel.send(embed=message)


def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))
