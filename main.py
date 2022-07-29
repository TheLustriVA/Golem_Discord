import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
import json
import openai
"""
Define a python class for a Discord bot using the discord.py 1.7.3 API. The class should be able connect to the Discord server with ID 851041307493138432 using a token stored in the DISCORD_TOKEN value in a .env file. The bot's name is Golem. The class must be able to load extensions and register cogs.
"""

intents = discord.Intents.default()
intents.members = True

env_path = '.env'
load_dotenv(dotenv_path=env_path)

description = """
Golem is a bot that can be used to manage the server.
"""

openai.api_key = os.getenv("OPENAI_API_KEY")

async def get_ai_response(message):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"The following is a conversation with an AI assistant named Golem. Golem is evasive, creative, clever, and snarky. {message}",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0.3,
        presence_penalty=0.3
        )
    return response

async def get_greeting():
    with open("content/greetings.json", "r", encoding="utf-8") as f:
        greetings_blob = json.load(f)
        greet_switch = random.random_choice([True, False])
        if greet_switch:
            return random.choice(greetings_blob["greetings"])
        else:
            return random.choice(greetings_blob["glitches"])

class DiscordBot(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.channel.id == 873009485512323102:
            if message.content.startswith(">hello"):
                greeting = await get_ai_response()
                await message.channel.send(greeting)
        
        if message.content.startswith('>hello'):
            await message.channel.send(f"Heya. Sorry, I'm still lurking. I don't talk. I'm a bot. {get_greeting()}")

if __name__ == '__main__':
    bot = commands.Bot(command_prefix='>', description=description, intents=intents)
    bot.run(os.getenv("DISCORD_TOKEN"))