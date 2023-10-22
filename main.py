import asyncio
import logging
import os
import random

import aiohttp
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
OWNER = os.getenv("OWNER_ID")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", case_insensitive=True, owner_id=OWNER, intents=intents)
logging.basicConfig(level=logging.INFO)

async def load_cogs():
    for folder in os.listdir("cog_modules"):
        if os.path.exists(os.path.join("cog_modules", folder, "cog.py")):
            await bot.load_extension(f"cog_modules.{folder}.cog")
            print(f"{folder} loaded!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}!")
    game = discord.Game("hi!")
    await bot.change_presence(activity=game)
    await load_cogs() 


bot.run(TOKEN)
