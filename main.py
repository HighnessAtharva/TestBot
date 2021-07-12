"""
Importing Dependancies
"""

import discord
import os
import platform
import random
import json
import sys
import itertools
from itertools import cycle
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from keep_alive import keep_alive


"""
Bot Metadata
"""
description = '''A test bot developed by HighnessAlex and the Gang. 
                 Experimental stuff mostly.'''
prefix='!'
bot = commands.Bot(command_prefix=prefix, description=description )

#Removing the in-built bot 'help'
bot.remove_command("help")

"""
Purge Cuss Words and Restrict Blacklisted Users to message. The code in this event is executed every time someone sends a message, with or without the prefix
"""

@bot.event
async def on_message(message):
       
        # Ignores if a command is being executed by a bot or by the bot itself
        if message.author == bot.user or message.author.bot:
            return
        # Ignores if a command is being executed by a blacklisted user
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if message.author.id in blacklist["ids"]:
            return
        await bot.process_commands(message)
        with open('cuss.txt') as file:
            _file = file.read().split("\n")
        for badword in _file:
            if badword in message.content.lower():
                await message.delete()
                await message.channel.send(f'{message.author.mention}! Your message has not passed moderation!')
        
                
  

"""
Setting up Config Files
"""
if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

"""
Bot Status
"""
@tasks.loop(minutes=1.0)
async def status_task():
    statuses = ["Genshin Impact!", "Far Cry 6!", f"{config['bot_prefix']}help | Created by HighnessAlex", "with your heart!"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))

"""
--Events--
"""
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()


"""
Logging Command Executed History to Console
"""
@bot.event
async def on_command_completion(ctx):
    fullCommandName = ctx.command.qualified_name
    split = fullCommandName.split(" ")
    executedCommand = str(split[0])
    print(
        f"Executed {executedCommand} command in {ctx.guild.name} (ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})")



"""
Loading All Cogs
"""
if __name__ == "__main__":
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


"""
Commands
"""
@bot.command(aliases=['clr'])
async def clear(context, amount=5):
	await context.channel.purge(limit=amount)




"""
Error Handing Event
"""
@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="Hey, please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission `" + ", ".join(
                error.missing_perms) + "` to execute this command!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            description=str(error).capitalize(),
            # We need to capitalize because the command arguments have no capital letter in the code.
            color=0xE02B2B
        )
        await context.send(embed=embed)
    raise error
keep_alive()
my_secret = os.environ['TOKEN']
bot.run(my_secret)
