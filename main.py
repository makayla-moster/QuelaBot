import asyncio
import logging
import os
import random

import aiohttp
import disnake
from disnake.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
OWNER = os.getenv("OWNER_ID")
bot = commands.Bot(command_prefix="!", case_insensitive=True, owner_id=OWNER)
logging.basicConfig(level=logging.INFO)

for folder in os.listdir("cog_modules"):
    if os.path.exists(os.path.join("cog_modules", folder, "cog.py")):
        bot.load_extension(f"cog_modules.{folder}.cog")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}!")
    game = disnake.Game("with AoE2 data")
    await bot.change_presence(activity=game)


bot.run(TOKEN)
