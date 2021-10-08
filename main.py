import discord
import random
from discord.ext import commands

from pwdFactory.pwdFactory import getPwdList
from store import pwdStore

bot = commands.Bot(command_prefix='$')
psm = pwdStore()

@bot.command()
async def new(ctx, account, box):
    """
    makes new password attached to the user account ACCOUNT on the machine BOX.
    """
    pwd = getPwdList(1)

    psm.addPwd(account, box, pwd)
    await ctx.send('Added: ' + psm.prettyGetPwd(account, box))

f = open('secrets.txt')
secret = f.read()
bot.run(secret)
