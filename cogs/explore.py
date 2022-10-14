import os

import discord
import httpx
from discord.ext import commands
from dotenv import load_dotenv

env_path = "../.env"  # Load the bot's token from the .env file
load_dotenv(dotenv_path=env_path)

class Astronomy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nasa_api_key = os.getenv("NASA_API_KEY")
        self.nasa_endpoints = { 
                               "APOD" : "https://api.nasa.gov/planetary/apod",
                               "LS_Imagery" : "https://api.nasa.gov/planetary/earth/imagery",
                               "LS_Assets" : "https://api.nasa.gov/planetary/earth/assets",
                               "CME_Analysis" : "https://api.nasa.gov/DONKI/CMEAnalysis",
                               "CME" : "https://api.nasa.gov/DONKI/CME",
                               "GST" : "https://api.nasa.gov/DONKI/GST",
                               "Solar_Flare" : "https://api.nasa.gov/DONKI/FLR",
                               }

    # define a function called lon_lat_val() that will validate the user's input for latitude and longitude
    async def lon_lat_val(self, latitude, longitude):
        if latitude is None or longitude is None:
            return False
        elif latitude < -90 or latitude > 90:
            return False
        elif longitude < -180 or longitude > 180:
            return False
        else:
            return True

    @commands.command()
    async def apod_by_date(self, ctx, date:str):
        """
        This command will return the Astronomy Picture of the Day for a given date - FORMAT: YYYY-MM-DD.
        """
        url = f"{self.nasa_endpoints['APOD']}"
        params = {"api_key": self.nasa_api_key, "date": date}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                response = response.json()
                embed = discord.Embed(title=response["title"], description=response["explanation"], color=0xd1c00c)
                embed.set_image(url=response["url"])
                await ctx.send(embed=embed)
            else:
                await ctx.send("There was an error. Please try again.")

    @commands.command()
    async def apod_by_daterange(self, ctx, start_date:str, end_date:str):
        """
        This command will return the Astronomy Picture of the Day between given dates - FORMAT: YYYY-MM-DD.
        """
        url = f"{self.nasa_endpoints['APOD']}"
        params = {"api_key": self.nasa_api_key, "start_date" : start_date, "end_date" : end_date}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                images = response.json()
                main_image = images[0]
                print(main_image)
                embed = discord.Embed(title=main_image["title"], description=main_image["explanation"], color=0xd1c00c)
                embed.set_image(url=main_image["url"])
                embed.set_thumbnail(url=main_image["url"])
                embed.add_field(name="Photo", value=main_image['copyright'], inline=True)
                embed.add_field(name="Date", value=main_image['date'], inline=True)
                for image in images[1:31]:
                    embed.add_field(name=image['date'], value=image['url'], inline=False)
                embed.set_footer(text=f"The daterange command will only return a calendar month of images: https://api.nasa.gov/")
                await ctx.send(embed=embed)
            else:
                await ctx.send("There was an error. Please try again.")

    @commands.command()
    async def earth_images(self, ctx, latitude, longitude, dim=0.25, date=None):
        """
        This command will return the Earth's imagery for a given date - FORMAT: YYYY-MM-DD.
        """
        url = f"{self.nasa_endpoints['LS_Imagery']}"
        if date is None:
            params = {"api_key": self.nasa_api_key, "lat": latitude, "lon": longitude, "dim": dim}
        elif date is not None:
            params = {"api_key": self.nasa_api_key, "lat": latitude, "lon": longitude, "date": date, "dim": dim}
        elif latitude is None or longitude is None or self.lon_lat_val(latitude, longitude) is False:
            await ctx.send("Please enter a latitude and longitude.")
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                response = response.json()
                embed = discord.Embed(title=response["title"], description=response["explanation"], color=0xd1c00c)
                embed.set_image(url=response["url"])
                embed.add_field(name="Photo", value=response['copyright'], inline=True)
                embed.add_field(name="Date", value=response['date'], inline=True)
                embed.set_footer("https://api.nasa.gov/")
                await ctx.send(embed=embed)
            else:
                await ctx.send("There was an error. Please try again.")

    @commands.command()
    async def CME_analysis(self, ctx, latitude, longitude, dim=0.25, date=None):
        """
        This command will return the Earth's imagery for a given date - FORMAT: YYYY-MM-DD.
        """
        url = f"{self.nasa_endpoints['LS_Imagery']}"
        if date is None:
            params = {"api_key": self.nasa_api_key, "lat": latitude, "lon": longitude, "dim": dim}
        elif date is not None:
            params = {"api_key": self.nasa_api_key, "lat": latitude, "lon": longitude, "dim": dim, "date": date}
        elif latitude is None or longitude is None or self.lon_lat_val(latitude, longitude) is False:
            await ctx.send("Please enter a latitude and longitude.")
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                response = response.json()
                embed = discord.Embed(title=response["title"], description=response["explanation"], color=0xd1c00c)
                embed.set_image(url=response["url"])
                embed.add_field(name="Photo", value=response['copyright'], inline=True)
                embed.add_field(name="Date", value=response['date'], inline=True)
                embed.set_footer("https://api.nasa.gov/")
                await ctx.send(embed=embed)
            else:
                await ctx.send("There was an error. Please try again.")

    @commands.command()
    async def CME_analysis(self, ctx, starDate=None, endDate=None, speed=0, halfAngle=0, catalog="All", keyword=None):
        """
        This command will return the Earth's imagery for a given date - FORMAT: YYYY-MM-DD.
        """
        url = f"{self.nasa_endpoints['CME_Analysis']}"
        params = {"api_key": self.nasa_api_key, "start_date" : starDate, "end_date" : endDate, "speed" : speed, "half_angle" : halfAngle, "catalog" : catalog, "keyword" : keyword}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                response = response.json()
                embed = discord.Embed(title=response["title"], description=response["note"], color=0xd1c00c)
                embed.set_image(url=response["url"])
                embed.set_footer("https://api.nasa.gov/")
                await ctx.send(embed=embed)
            else:
                await ctx.send("There was an error. Please try again.")



async def setup(bot):
    bot.add_cog(Astronomy(bot))