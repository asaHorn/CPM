import discord
import random
from pswdFactory.pswdFactory import getPswdList

description = '''Asa's bot for fucking around with stuff'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='$', description=description, intents=intents)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello World! I made this just for you... ' + getPswdList(1))


f = open('secrets.txt')
secret = f.read()
bot.run(secret)
