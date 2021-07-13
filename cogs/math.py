import os
import sys
import json
import discord
from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

class math(commands.Cog, name="math"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases = ['evaluate'])
    async def eval(self, ctx, *, equation):
      allOperators = ['+', '-', '*', '/', '^', '%', '=', '>=', '<=', '>', '<']
      operator = ''
      for x in allOperators:
        if x in equation:
          operator = x
      
      equation = equation.split(operator)
      num1, num2 = float(equation[0]), float(equation[1])
      result = {'+':lambda x,y:x+y,'-':lambda x,y:x-y,'*':lambda x,y:x*y,'/':lambda x,y:x/y,'^':lambda x,y:x**y,'%':lambda x,y:x%y,'=':lambda x,y:x==y,'>':lambda x,y:x>y,'<':lambda x,y:x<y,'>=':lambda x,y:x>=y,'<=':lambda x,y:x<=y}[operator](num1,num2)
      if result % 1 == 0:
        result = int(result)
      await ctx.send(f"{ctx.author.mention}, **Result:** ``{result}``")

    # Addition (+)
    @commands.command(aliases=['addition'])
    async def add(self, ctx, num1: int, num2: int):
        result = num1 + num2
        await ctx.send(f"Result of addition: {result}")

    # Subtraction (-)
    @commands.command(aliases=['subtraction'])
    async def sub(self, ctx, num1: int, num2: int):
        the_result = num1 - num2
        await ctx.send(f"Result of subtraction: {the_result}")

    # Division (/,÷)  
    @commands.command(aliases=['division'])
    async def div(self, ctx, num1: int, num2: int, *, rounded = False):
  
        if rounded == False:
            res = num1 / num2
            await ctx.send(f"Result of division: {res}")
  
        else:
            res = num1 // num2
            await ctx.send(f"Result: {res}")
    
    # Multiplication (x)  
    @commands.command(aliases=['multiplication'])
    async def mul(self, ctx, num1: int, num2: int):
        res = num1 * num2
        await ctx.send(f"Result of multiplication: {res}")

def setup(bot):
    bot.add_cog(math(bot))