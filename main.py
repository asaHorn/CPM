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
    if the account box combo already has a password will override it and state the old password
    """
    account = account.lower()
    box = box.lower()
    pwd = getPwdList(1)

    if psm.exists(account, box):
        old = psm.getPwd(account, box)
        psm.addPwd(account, box, pwd)
        await ctx.send('Changed: ' + psm.makeID(account, box) + ' ' +
                       old + ' --> ' + psm.getPwd(account, box))
        await ctx.send('Remember to update password in scoring or CPM will be sad :(')
        return

    psm.addPwd(account, box, pwd)
    await ctx.send('Added: ' + psm.prettyGetPwd(account, box))


@bot.command()
async def get(ctx, account, box):
    """
    send the requested user / box record to discord
    """
    await ctx.send(psm.prettyGetPwd(account, box))


@bot.command()
async def list(ctx):
    """
    print out a pretty table of all tracked passwords
    """
    dump = psm.dump()
    if dump == "{}":
        await ctx.send('I am not tracking any passwords')
        return

    dump = dump.strip(' ')
    dumpList = dump[1:-1].split(',')  # [1,-1] chops out {}s

    ret = "```"
    i = 0
    for x in dumpList:
        elements = x.split(':')
        ret += str(i) + '. ' + elements[0] + getSpacing(elements[0], 70) \
               + getSpacing(elements[1], 70) + elements[1] + '\n'
        i += 1
    ret += "```"
    await ctx.send(ret)


# todo add history

# todo add back up

# todo add auto updated list


##########################################################
##Helper functions###
##########################################################
def getSpacing(s: str, tLen: int):
    ret = ""
    for _ in range(tLen - len(s)):
        ret += ' '
    return ret


f = open('secrets.txt')
secret = f.read()
bot.run(secret)
