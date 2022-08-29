import httpx
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

env_path = "../.env"  # Load the bot's token from the .env file
load_dotenv(dotenv_path=env_path)

class Stable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        


async def setup(bot):
    bot.add_cog(Stable(bot))