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
    
    @commands.command()
    async def warn(self, ctx, offender_id, post_url, warning_given, punishment, summary, description, comments):
        """
        This command will warn a user and store the warning in the database.
        """
        conn = psycopg2.connect(user=self.psql_user, password=self.psql_password, database='mod_tools', host=self.psql_url, port=self.psql_port)
        async with conn.cursor() as cur:
            warn_insert = f"INSERT INTO warnings ({ctx.message.id}, {ctx.message.author.name}, {offender_id}, {post_url}, {warning_given}, {punishment}, {summary}, {description}, {comments})"
            await cur.execute()
            await conn.commit()
            await cur.close()
            await conn.close()
            print(warn_insert)
        await ctx.send("Warning recorded.")
        
def setup(bot):
    bot.add_cog(Warnings(bot))