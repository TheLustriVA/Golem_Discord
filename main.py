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

bot_invite_url = "https://discord.com/api/oauth2/authorize?client_id=710056301195165768&scope=bot&permissions=8"

intents = discord.Intents.default()
intents.members = True

env_path = '.env'
load_dotenv(dotenv_path=env_path)

description = """
Golem is a bot that can be used to manage the server.
"""

openai.api_key = os.getenv("OPENAI_API_KEY")

bot = commands.Bot(command_prefix='>', description=description, intents=intents)

# define a bot event that waits for a message in a channel and then responds with a greeting from the openai chatbot API

async def get_openai_API_greeting(message):
    response = openai.Completion.create(engine="text-davinci-002", prompt=f"The following is a response from an AI chatbot named Golem. The chatbot is clever, creative, and unhelpful. It is responding to the human saying: {str(message)}", max_tokens=256)
    return response.choices[0].text


async def get_greeting():
    with open("content/greetings.json", "r", encoding="utf-8") as f:
        greetings_blob = json.load(f)
        greet_switch = random.choice([True, False])
        if greet_switch:
            # return a random greeting from greetings.human_greetings in greetins.json
            return random.choice(greetings_blob['greetings']["human_greetings"])
        else:
            return random.choice(greetings_blob['greetings']["glitches"])

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    allowed_channels = [873009485512323102, 868690558716108831]
    
    if message.channel.id in allowed_channels:
        if message.content.startswith(">hello"):
            await message.channel.send("API response fired off.")
            greeting = await get_openai_API_greeting(message.content)
            await message.channel.send(greeting)
    elif message.channel.id not in allowed_channels:
        if message.content.startswith('>hello'):
            await message.channel.send(f"Heya. Sorry, I'm still lurking. I don't talk. I'm a bot. {await get_greeting()}")

if __name__ == '__main__':
    bot.run(os.getenv("DISCORD_TOKEN"))