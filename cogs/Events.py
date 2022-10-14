import os
from typing import Optional

import discord
import jsonlines
import redis
import redis.commands.search.aggregation as aggregations
from redis.commands import search
from redis.commands.search import field
from redis.commands.search import indexDefinition
from redis.commands.search import reducers
from discord.ext import commands
from dotenv import load_dotenv
from redis.commands.json.path import Path
from redis.commands.search.field import NumericField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query

env_path = ".env"  # Load the bot's token from the .env file
load_dotenv(dotenv_path=env_path)

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.redis_url = "localhost"
        self.redis_port = 6379
        self.redis_user = "gf_admin" 
        self.redis_password = os.getenv("REDIS_PASSWORD")
        
    @commands.command()
    async def warn(self, ctx, offender_id, post_url, warning_given, punishment, summary, description, comments):
        """
        This command will warn a user and store the warning in the database.
        """
        r = redis.from_url("redis://{self.redis_user}:{self.redis_password}@{self.redis_url}:{self.redis_port}/0")
        
        async with r.pipeline(Transaction=True) as pipe:
            warning = {
                "altercation" :
                    {
                    "moderator_id" : ctx.author.id,
                    "moderator_name" : ctx.author.name,
                    "offender_id" : offender_id,
                    "date_time" : ctx.message.created_at,
                    "post_url": post_url,
                    "warning" : warning_given,
                    "punishment" : punishment,
                    "offence_type" : summary,
                    "offence_description" : description,
                    "comments" : comments    
                    }
            }
            r.json().set("warning_record", Path.root_path(), warning)
            
            schema = (NumericField("$.altercation.moderator_id", as_name="moderator_id"), TextField("$.altercation.moderator_name", as_name="moderator_name"), NumericField("$.altercation.offender_id", as_name="offender_id"), TextField("$.altercation.post_url", as_name="post_url"), TextField("$.altercation.date_time", as_name="date_time"), TextField("$.altercation.warning", as_name="warning"), TextField("$.altercation.punishment", as_name="punishment"), TextField("$.altercation.offence_type", as_name="offence_type"), TextField("$.altercation.offence_description", as_name="offence_description"), TextField("$.altercation.comments", as_name="comments"))
            r.ft().create_index(schema, definition=IndexDefinition(prefix=["warning_record:"], index_type=IndexType.JSON))


def setup(bot):
    bot.add_cog(Events(bot))