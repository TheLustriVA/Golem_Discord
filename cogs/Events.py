import datetime
import os
from typing import Optional

import discord
import jsonlines
from discord.ext import commands
from dotenv import load_dotenv
from pydantic import ValidationError
from redis_om import Field, HashModel, get_redis_connection

env_path = ".env"  # Load the bot's token from the .env file
load_dotenv(dotenv_path=env_path)

class Prompt(HashModel):
    moderator_name: str = Field(index=True)
    moderator_id: int = Field(index=True)
    offender_id: int = Field(index=True)
    post_url: str = Field(index=True)
    warning: str = Field(index=True)
    date_time: datetime.datetime = Field(index=True)
    action_taken: str
    offence_type: str
    offence_description: str = Field(index=True)
    comments: Optional[str] = "No comments"

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.redis_url = "localhost"
        self.redis_port = 6379
        self.redis_user = "gf_admin" 
        self.redis_password = os.getenv("REDIS_PASSWORD")
        
    @commands.Command()
    async def warn(self, message: discord.Message, offender_id: int, post_url: str, warning: str, date_time: datetime.datetime, action_taken: str, offence_type: str, offence_description: str, comments: Optional[str] = "No comments"):
        """_
        Gather the messages sent in the bot's channels and store them in a JSONL file_
        """
        if message.author.bot:
            return None
        else:
            redis = get_redis_connection(f"redis://[{self.redis_user}:{self.redis_password}]@{self.redis_url}:{self.redis_port}/0")
            try:
                Prompt(
                    moderator_name=message.author.name,
                    moderator_id=message.author.id,
                    offender_id=offender_id,
                    post_url=post_url,
                    warning=warning,
                    date_time=datetime.datetime.strptime(date_time, "%m/%d/%Y %H:%M:%S"),
                    action_taken=action_taken,
                    offence_type=offence_type,
                    offence_description=offence_description,
                    comments=comments
                ).save(redis)
            except ValidationError as e:
                print(e)
                

def setup(bot):
    bot.add_cog(Events(bot))