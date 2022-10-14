import os

import discord
import jsonlines
import openai
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound
from dotenv import load_dotenv

from cogs.Events import Events
from cogs.explore import Astronomy

bot_invite_url = "https://discord.com/oauth2/authorize?client_id=1029801423522779236&permissions=8&scope=bot"  # set the bot's invite url

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True, message_content=True, typing=True, voice_states=True, webhooks=True)  # set the intents for the bot


env_path = ".env"  # Load the bot's token from the .env file
load_dotenv(dotenv_path=env_path)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

description = """
Golem is an echo of the Essai who has gone on to greater duties.
"""  # Set the bot's description

openai.api_key = os.getenv("OPENAI_API_KEY")  # Set the OpenAI API key


bot = commands.Bot(
    command_prefix="+", description=description, intents=intents
)  # Create the bot

#bot.add_cog(TTS(bot))




async def get_openai_API_greeting(message: str) -> str:
    """_Take the contents of messages starting with '>hello' in certain channels and pulls a response from GPT-3_

    Args:
        message (_type_): _A string of the message contents to which the bot should respond_

    Returns:
        _str_: _A string response to the message taken from the GPT-3 API_
    """
    response = openai.Completion.create(
        engine="text-davinci-002",

        prompt=f"The following is a response from an AI chatbot named Pippa. The chatbot is girly, perky, creative, and helpful. It is responding to the human saying: {str(message)}",
        max_tokens=512
    )  # Create a response from the OpenAI API
    return response.choices[0].text  # Return the first response from the API


@bot.event
async def on_ready():  # When the bot is ready
    print(f"{bot.user.name} has connected to Discord!")  # Print the bot's name and connection status
    await bot.add_cog(Astronomy(bot))
    await bot.add_cog(Events(bot))


@bot.event
async def on_member_join(member):
    await member.send(f'Welcome to Unstable Diffusion, {member.mention}! Enjoy your stay here!')

# button code
class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="", row=0, style=discord.ButtonStyle.primary, emoji="⭐")
    async def button_callback(self, button, interaction):
        # todo code here to add photo to star leaderboard and possibly a dataset
        await interaction.response.send_message("You clicked the star button!") # Send a message when the button is clicked


    @discord.ui.button(label="Upscale", row=0, style=discord.ButtonStyle.primary, emoji="⏩")
    async def upscale_button_callback(self, button, interaction):
        # todo rerun the prompt given before with upscaling... this is gonna suck.
        await interaction.response.send_message("You clicked the upscale button!")  # Send a message when the button is clicked


    @discord.ui.button(label="Report", row=0, style=discord.ButtonStyle.primary, emoji="🚩")  # Create a button with the label "😎 Click me!" with color Blurple
    async def report_button_callback(self, button, interaction):
        # todo should send image to be checked immediately
        await interaction.response.send_message("You clicked the report button! Thanks for keeping an eye on things!")  # Send a message when the button is clicked

    @bot.command()
    async def rapsheet(ctx, user_id):
        """Get the user's rap sheet"""
        print("Something")
        embed=discord.Embed(title=f"Report for <@{user_id}>", url="https://api.farq2.xya", description="Moderation and warnings report")
        embed.set_author(name=f"<@{user_id}>", url="https://genfactory.ai/TermsOfService", icon_url="https://i.imgur.com/A69SwSP.png")
        embed.set_thumbnail(url="https://i.imgur.com/VRDdF1U.png")
        embed.add_field(name="User", value=f"<@{user_id}>", inline=False)
        embed.add_field(name="Discord User ID", value="695895956075446304", inline=False)
        embed.add_field(name="Date (d.m.y)", value="29.8.2022", inline=False)
        embed.add_field(name="Action taken", value="1h timeout", inline=False)
        embed.add_field(name="Summary", value="Celeb NSFW", inline=False)
        embed.add_field(name="Offense description", value="!draw donald trump naked", inline=False)
        embed.add_field(name="Reporter", value="Appreciator#6332", inline=False)
        embed.add_field(name="Additional comments", value="...", inline=False)
        embed.set_footer(text="Unstable diffusion server - User log offenses ban and timeout")
        await ctx.send(embed=embed)

    @bot.command()
    async def hey(ctx, user_id, *, message):
        """Record a warning"""
        print("Go!")
        print({'user': user_id, 'message': message, 'reporter': ctx.author.id})
        with jsonlines.open('warnings.jsonl', mode='a') as writer:
            writer.write({'user': user_id, 'message': message, 'reporter': ctx.author.id})

@bot.command()
async def ping(ctx):
    """Ping the bot"""
    print("Command heard")
    await ctx.send("Pong!")

@bot.event
async def on_message(message: discord.Message):  # When a message is sent

    if message.author == bot.user:  # If the message is from the bot
        return  # Return nothing
    # else:
    #     if "Pippa" in message.content and message.content.endswith("?") or message.content.endswith("..."):  # If the message starts with '>hello'
    #         greeting = await get_openai_API_greeting(message.content)  # Get a greeting from the OpenAI API
    #         await message.channel.send(greeting.replace("Pippa:\n", ""))  # Send the API greeting to the channel
    #         print(f"{message.channel.name} - {message.author.name} - {message.content}")
    await bot.process_commands(message)  # Process commands
        
    


if __name__ == "__main__":  # If the bot is being run directly
    try:
        print("The bot is connecting to Discord!")
        bot.run(DISCORD_TOKEN)  # Run the bot
    except Exception as e:
        print(e)