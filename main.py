import discord
import random
from discord.ext import commands

from pswdFactory.pswdFactory import getPswdList

bot = commands.Bot(command_prefix='$CPM ')


@bot.event
async def onReady():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def newPass(ctx, amount):
    await ctx.send(getPswdList(int(amount)))

f = open('secrets.txt')
secret = f.read()
bot.run(secret)
