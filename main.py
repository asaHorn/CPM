import discord
from discord.ext import commands

from pwdFactory.pwdFactory import getPwdList
from store import pwdStore
from randomStorage import randomStorage

bot = commands.Bot(command_prefix='$')
psm = pwdStore()
ram = randomStorage()


@bot.command()
async def addTopo(ctx, *args):
    send = ''
    for x in args:
        send += x + ' '

    await ctx.send(psm.addTopo(send))

@bot.command()
async def list(ctx):
    """
    makes a new auto-updated list of all tracked passwords
    """
    embed = discord.Embed(title="source", url="https://github.com/asaHorn/CPM",
                          description="If you see this CPM is fucked", color=0xff0000)
    embed.set_author(name="CPM")

    ram.displayMessage = await ctx.send(embed=embed)
    await ram.displayMessage.edit(embed=psm.display())


@bot.command()
async def new(ctx, box, user, *args):
    """
    makes new password attached to the user account ACCOUNT on the machine BOX.
    if the account box combo already has a password will override it and state the old password

    usage:
    $new box user <note1>,<note2> <note3>....
        Special notes:
        -^(note) will cause all passwords tagged with this note to be displayed separately
        -admin will cause user to be bolded on list
        -any other notes will appear in the Notes heading on display
    """
    user = user.lower()
    box = box.lower()
    pwd = getPwdList(1)
    tagList = []

    for entry in args:
        tagList += entry.split(',')

    for tag in tagList:
        tag = tag.lower()

    if psm.exists(user, box):
        old = psm.getPwd(user, box)
        psm.addPwd(user, box, pwd, tagList)
        await ctx.send('Changed: ' + psm.makeID(user, box) + ' ' +
                       old + ' --> ' + psm.getPwd(user, box))
        await ctx.send('Remember to update password in scoring or CPM will be sad :(')
    else:
        errors = psm.addPwd(user, box, pwd, tagList)
        if errors != '``````':
            await ctx.send(errors)
            if errors[0:26] == 'Unable to add password...':
                return
        await ctx.send('Added: ' + psm.prettyGetPwd(user, box))

    if ram.displayMessage == '':
        await ctx.send("I can't find an active display, use $list to fix this")
        return
    await ram.displayMessage.edit(embed=psm.display())


@bot.command()
async def get(ctx, box, user):
    """
    send the requested user / box record to discord
    """
    await ctx.send(psm.prettyGetPwd(user, box))

# todo add history

# todo add back up

##########################################################
# Helper functions #
##########################################################
def getSpacing(s: str, tLen: int=35):
    ret = ""
    for _ in range(tLen - len(s)):
        ret += ' '
    return ret

f = open('secrets.txt')
secret = f.read()
bot.run(secret)
