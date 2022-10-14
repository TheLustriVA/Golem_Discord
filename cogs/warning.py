import os

import discord
import psycopg2
from discord.ext import commands


class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.psql_url = "localhost"
        self.psql_port = 5432
        self.psql_user = "mod_tools" 
        self.psql_password = os.getenv("PSQL_PASSWORD")
        
    async def db_connect(self):
        conn = await psycopg2.connect(user=self.psql_user, password=self.psql_password, database='mod_tools', host=self.psql_url, port=self.psql_port)
        return conn
    
    @commands.command()
    async def warn(self, ctx, offender_id, post_url, warning_given, punishment, summary, description, comments):
        """
        This command will warn a user and store the warning in the database.
        """
        conn = await self.db_connect()
        async with conn.cursor() as cur:
            await cur.execute(f"INSERT INTO warnings ({ctx.message.id}, {ctx.message.author.name}, {offender_id}, {post_url}, {ctx.message.content}, {punishment}, {summary}, {description}, {comments})")
            await conn.commit()
            await cur.close()
            await conn.close()
            
        await ctx.send("Warning recorded.")