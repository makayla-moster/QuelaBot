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
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

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
