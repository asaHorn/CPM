import discord
from pswdFactory.pswdFactory import getPswdList

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello World!, I made this just for you... ' + getPswdList(1))


f = open('secrets.txt')
print('Hi, I need to make changes to this file as a test')
secret = f.read()
client.run('secret')
