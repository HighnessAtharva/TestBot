import json
import os
import platform
import random
import sys
import discord
from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

"""
General Commands Code Below. Implemented by inheriting the Cogs class
"""
class general(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", aliases=["botinfo"])
    async def info(self, context):
        """
        Get some useful (or not) information about the bot.
        """
        embed = discord.Embed(
            description="This is just a test bot, might be a bit degenerate. :p",
            color=0x42F56C
        )
        embed.set_author(
            name="Bot Info"
        )
        embed.add_field(
            name="Owner:",
            value="HighnessAlex#6480",
            inline=True
        )
        embed.add_field(
            name="Python Version:",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"{config['bot_prefix']}",
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {context.message.author}"
        )
        await context.send(embed=embed)
        
    """
    Get some useful (or not) information about the server.
    """
            
    @commands.command(name="server",aliases=["serverinfo"])
    async def serverinfo(self, context):
            server = context.message.guild
            roles = [x.name for x in server.roles]
            role_length = len(roles)
            if role_length > 50:
                roles = roles[:50]
                roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
            roles = ", ".join(roles)
            channels = len(server.channels)
            time = str(server.created_at)
            time = time.split(" ")
            time = time[0]

            embed = discord.Embed(
                title="**Server Name:**",
                description=f"{server}",
                color=0x42F56C
            )
            embed.set_thumbnail(
                url=server.icon_url
            )
            embed.add_field(
                name="Owner",
                value=f"HighnessAlex#6480"
            )
            embed.add_field(
                name="Server ID",
                value=server.id
            )
            embed.add_field(
                name="Member Count",
                value=server.member_count
            )
            embed.add_field(
                name="Text/Voice Channels",
                value=f"{channels}"
            )
            embed.add_field(
                name=f"Roles ({role_length})",
                value=roles
            )
            embed.set_footer(
                text=f"Created at: {time}"
            )
            await context.send(embed=embed)

    @commands.command(name="ping")
    async def ping(self, context):
        """
        Check if the bot is alive.
        """
        latency=round(self.bot.latency)
        verdictList=["Poor", "OK", "Great!"]
        verdict=None
        if latency>=800:
            verdict=verdictList[0]
        elif latency>300 and latency<800:
            verdict=verdictList[1]
        else:
            verdict=verdictList[2]
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {latency*1000}ms. {verdict}",
            color=0x42F56C
        )
        await context.send(embed=embed)



    """
    Get the invite link of the bot to be able to invite it.
    """
    @commands.command(name="invite")
    async def invite(self, context):

        embed = discord.Embed(
            description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id={config['application_id']}&scope=bot&permissions=470150263).",
            color=0xD75BF4
        )
        try:
            # To know what permissions to give to your bot, please see here: https://discordapi.com/permissions.html and remember to not give Administrator permissions.
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)

        """
        Create a poll where members can vote.
        """
    @commands.command(name="poll", aliases=["vote"])
    async def poll(self, context, *, title):

        embed = discord.Embed(
            title="A new poll has been created!",
            description=f"{title}",
            color=0x42F56C
        )
        embed.set_footer(
            text=f"Poll created by: {context.message.author} • React to vote!"
        )
        embed_message = await context.send(embed=embed)
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")
        await embed_message.add_reaction("🤷")


def setup(bot):
    bot.add_cog(general(bot))