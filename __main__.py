import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import os
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
APPLICATION_ID = int(os.getenv('APPLICATION_ID'))

discord.utils.setup_logging(level=logging.INFO, root=True)
bot = commands.AutoShardedBot(intents=discord.Intents.all(), command_prefix="/", application_id=APPLICATION_ID)

@bot.event
async def on_ready():
    await bot.tree.sync()
    logging.info(f"{bot.user} now is online!")


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            if filename != '__init__.py':
                await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    await load()
    await bot.start(TOKEN)


asyncio.run(main())