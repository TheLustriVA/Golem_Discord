"""
Bot name: Golem
Bot description: A chatbot that is clever, creative, and unhelpful.
Bot author: Marco Lustri
Bot version: 1.0.0
Bot license: MIT

Description: This is the main file for the bot. It is responsible for handling the bot's commands and responses.
"""

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
import json
import openai


bot_invite_url = "https://discord.com/api/oauth2/authorize?client_id=710056301195165768&scope=bot&permissions=8"  # set the bot's invite url

intents = discord.Intents.default()  # Set the bot's intents
intents.members = True  # Include the 'members' privedged intent

env_path = ".env"  # Load the bot's token from the .env file
load_dotenv(dotenv_path=env_path)

description = """
Golem is a bot that can be used to manage the server.
"""  # Set the bot's description

openai.api_key = os.getenv("OPENAI_API_KEY")  # Set the OpenAI API key

bot = commands.Bot(
    command_prefix=">", description=description, intents=intents
)  # Create the bot


async def get_openai_API_greeting(message: str) -> str:
    """_Take the contents of messages starting with '>hello' in certain channels and pulls a response from GPT-3_

    Args:
        message (_type_): _A string of the message contents to which the bot should respond_

    Returns:
        _str_: _A string response to the message taken from the GPT-3 API_
    """
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"The following is a response from an AI chatbot named Golem. The chatbot is clever, creative, and unhelpful. It is responding to the human saying: {str(message)}",
        max_tokens=256,
    )  # Create a response from the OpenAI API
    return response.choices[0].text  # Return the first response from the API


async def get_greeting():
    """_Returns a greeting from content/greetings.json for all channels not serviced by GPT-3_

    Returns:
        _str_: _Coinflip between a funny written response and a funny glitch response._
    """
    with open("content/greetings.json", "r", encoding="utf-8") as f:  # Open the file
        greetings_blob = json.load(f)  # Load the file
        greet_switch = random.choice([True, False])  # Coinflip
        if greet_switch:  # If the coinflip is true
            # return a random greeting from greetings.human_greetings in greetins.json
            return random.choice(
                greetings_blob["greetings"]["human_greetings"]
            )  # Return a random greeting
        else:  # If the coinflip is false
            return random.choice(
                greetings_blob["greetings"]["glitches"]
            )  # Return a random glitch


@bot.event
async def on_ready():  # When the bot is ready
    print(
        f"{bot.user.name} has connected to Discord!"
    )  # Print the bot's name and connection status


@bot.event
async def on_message(message: discord.Message):  # When a message is sent
    """__define a bot event that waits for a message in a channel and then responds with a greeting from the openai chatbot API__

    Args:
        message (_discord.Message): _A message object sent by a user in the server._
    """
    if message.author == bot.user:  # If the message is from the bot
        return  # Return nothing

    allowed_channels = [
        873009485512323102,
        868690558716108831,
    ]  # Set the channels that the bot will respond to with a GPT-3 response

    if (
        message.channel.id in allowed_channels
    ):  # If the message is in one of the allowed channels
        if message.content.startswith(">hello"):  # If the message starts with '>hello'
            await message.channel.send(
                "API response fired off."
            )  # Send a message to the channel
            greeting = await get_openai_API_greeting(
                message.content
            )  # Get a greeting from the OpenAI API
            await message.channel.send(greeting)  # Send the API greeting to the channel
    elif (
        message.channel.id not in allowed_channels
    ):  # If the message is not in one of the allowed channels
        if message.content.startswith(">hello"):  # If the message starts with '>hello'
            await message.channel.send(
                f"Heya. Sorry, I'm still lurking. I don't talk. I'm a bot. {await get_greeting()}"
            )  # Send a pre-written message to the channel


if __name__ == "__main__":  # If the bot is being run directly
    bot.run(os.getenv("DISCORD_TOKEN"))  # Run the bot
