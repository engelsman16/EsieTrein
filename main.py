from datetime import datetime
from config import settings
import discord
import os
import asyncio
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} Initialised {datetime.now()}")


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded {filename[:-3]}")


async def main():
    await load()
    await bot.start(settings.TOKEN)


asyncio.run(main())
