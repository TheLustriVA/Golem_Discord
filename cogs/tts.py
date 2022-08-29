from pathlib import Path
import torch
import torchaudio
import torch.nn as nn
import torch.nn.functional as F
import discord
from discord.ext import commands
import asyncio
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice, load_voices

# This will download all the models used by Tortoise from the HuggingFace hub.


class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tortoise_path = Path("F:\\dogma\\CentralDogma\\voices\Tortoise")
        self.voice_path = Path("F:\\dogma\\CentralDogma\\voices\\Tortoise\\tortoise-tts\\tortoise\\voices")
        self.tts = TextToSpeech()

    @commands.command()
    async def get_voices(self, ctx):
        """Gets all voices available through Tortoise"""
        voice_paths = [x for x in self.voice_path.iterdir() if x.is_dir()]
        for voice_dir in voice_paths:
            await ctx.send(voice_dir.name)   

    @commands.command()
    async def tts(self, ctx, *, text):
        """
        This command will convert text to speech.
        """
        # voice_choices = await self.get_voices(ctx)
        # def check(message):
        #     return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id and message.content.lower() in voice_choices
        # 
        # try:
        #     voice = await ctx.wait_for('message', check=check, timeout=60.0)
        # except asyncio.TimeoutError:
        #     await ctx.send("You took too long to respond. Try again.")
        #     return
        # voice = await load_voice("train_grace", "tortoise_tts")
        await ctx.send(file=discord.File(await self.tts.generate_audio(text, "train_grace"), "tts.mp3"))


    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")





async def setup(bot):
    bot.add_cog(TTS(bot))