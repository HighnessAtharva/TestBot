import json
import os
import platform
import random
import typing
import sys
import discord
import requests
from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

class imdb(commands.Cog, name="imdb"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="imdb", aliases=["movieinfo"])
    async def imdb(self, ctx, year:typing.Optional[int]=None, *, _name:str):
        """
        Fetches general info for a movie. Name-> Required, Year->Optional
        """
       
        _name=_name.split()
        title=''
        for word in _name:
            title+=word
            title+='+'
        title=str(title[:-1])
        
        print(year)
        print(title)
        key=os.environ['omdb_api_key']
        URL = f'http://www.omdbapi.com/?apikey={key}&t={title}&y={year}'
        r = requests.get(URL)
        response = r.json()

        embed=discord.Embed(title='Movie/TV Info', description='All the cool stuff you need to know',color=0x5a00ad)
        embed.set_author(name='HighnessAtharva')
        embed.add_field(name='Title', value=response.get('Title'), inline=True)
        embed.add_field(name='Year', value=response.get('Released'), inline=True)
        embed.add_field(name='Rating', value=response.get('Rated'), inline=True)
        embed.add_field(name='Released', value=response.get('Released'), inline=True)
        embed.add_field(name='Actors', value=response.get('Actors'), inline=True)
        embed.add_field(name='Genre', value=response.get('Genre'), inline=True)
        embed.add_field(name='Director', value=response.get('Director'), inline=True)
        embed.add_field(name='BoxOffice', value=response.get('BoxOffice'), inline=True)
        embed.add_field(name='imdbRating', value=response.get('imdbRating'), inline=True)
        embed.add_field(name='Plot', value=response.get('Plot'), inline=True)
        embed.add_field(name='Runtime', value=response.get('Runtime'), inline=True)
        embed.set_footer(text='Brought to you by OMDb API')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(imdb(bot))