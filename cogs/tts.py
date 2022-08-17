from pathlib import Path
import torch
import torchaudio
import torch.nn as nn
import torch.nn.functional as F
import discord
from discord.ext import commands

from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice, load_voices

# This will download all the models used by Tortoise from the HuggingFace hub.


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tortoise_path = Path("F:\\dogma\\CentralDogma\\voices\Tortoise")
        self.voice_path = Path("F:\\dogma\\CentralDogma\\voices\\Tortoise\\tortoise-tts\\tortoise\\voices")
        self.tts = TextToSpeech()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}~')
        else:
            await ctx.send(f'Hello {member.name}... This feels familiar.')
        self._last_member = member