import discord
from discord.ext import commands
from time import localtime, strftime


from pwdFactory.pwdFactory import getPwdList
from store import pwdStore
from randomStorage import randomStorage

bot = commands.Bot(command_prefix='$')
psm = pwdStore()
ram = randomStorage()


@bot.command()
async def listHere(ctx):
    """
    sets the channel to send $list to.

    Usage: run this command in desired channel
    "$listHere"
    """
    embed = discord.Embed(title="source", url="https://github.com/asaHorn/CPM",
                          description="If you see this CPM is fucked", color=0xff0000)
    embed.set_author(name="CPM")

    ram.displayMessage = await ctx.send(embed=embed)
    print(ram.displayMessage)
    await ram.displayMessage.edit(embed=display())


@bot.command()
async def new(ctx, box, user):
    """
    makes new password attached to the user account ACCOUNT on the machine BOX.
    if the account box combo already has a password will override it and state the old password
    """
    user = user.lower()
    box = box.lower()
    pwd = getPwdList(1)

    if psm.exists(user, box):
        old = psm.getPwd(user, box)
        psm.addPwd(user, box, pwd)
        await ctx.send('Changed: ' + psm.makeID(user, box) + ' ' +
                       old + ' --> ' + psm.getPwd(user, box))
        await ctx.send('Remember to update password in scoring or CPM will be sad :(')
        await ram.displayMessage.edit(embed=display())
        return

    psm.addPwd(user, box, pwd)
    if display() == 10:
        ctx.send("I can't find an active display, use $listHere to fix this")
    await ctx.send('Added: ' + psm.prettyGetPwd(user, box))
    await ram.displayMessage.edit(embed=display())


@bot.command()
async def get(ctx, box, user):
    """
    send the requested user / box record to discord
    """
    await ctx.send(psm.prettyGetPwd(user, box))


@bot.command()
async def list(ctx):
    await ram.displayMessage.edit(embed=display())


@bot.command()
async def oldList(ctx):
    """
    print out a pretty table of all tracked passwords

    **older, try $list  instead**
    """
    dump = psm.dump()
    if dump == "{}":
        await ctx.send('I am not tracking any passwords')
        return

    dumpList = dump[1:-1].split(',')  # [1,-1] chops out {}s

    ret = "```"
    i = 0
    for x in dumpList:
        x = x.strip(' ')
        elements = x.split(':')
        ret += getSpacing(str(i), 3) + str(i) + '. ' + elements[0] + getSpacing(elements[0]) \
               + getSpacing(elements[1], 25) + elements[1] + '\n'
        i += 1
    ret += "```"
    await ctx.send(ret)

    # todo group entries by type (net, windows, linux) then location (cloud, LAN, other stuff) then by box.
    # todo colors
    # todo pretty headings


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


def display():
    dump = psm.dump()
    if dump == '{}':
        embed = discord.Embed(title="source", url="https://github.com/asaHorn/CPM",
                              description="CPM isn't currently tracking anything", color=0xff0000)
        embed.set_author(name="CPM")
        embed.set_footer(text="last updated: " + strftime("%I:%M:%S %p", localtime()))

    else:
        dumpList = dump[1:-1].split(',')  # [1,-1] chops out {}s

        i = 1
        counter = ""
        users = ""
        passwords = ""
        for x in dumpList:
            x = x.strip(' ')
            elements = x.split(':')
            counter += str(i) + '.\n'
            users += elements[0] + '\n'
            passwords += elements[1] + '\n'
            i += 1

        print(counter[-3])
        embed = discord.Embed(title="source", url="https://github.com/asaHorn/CPM",
                              description="CPM tracking " + counter[-3] + " passwords over ... systems", color=0xff0000)
        embed.set_author(name="CPM")
        embed.add_field(name="n", value=counter, inline=True)
        embed.add_field(name="User", value=users, inline=True)
        embed.add_field(name="Pass", value=passwords, inline=True)
        embed.set_footer(text="last updated: " + strftime("%I:%M:%S %p", localtime()))

    return embed


f = open('secrets.txt')
secret = f.read()
bot.run(secret)
