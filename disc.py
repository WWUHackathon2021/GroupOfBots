import discord
import os
import json

client = discord.Client()
TOKEN = "ODMwNDk3Nzc4NTY4Mzk2ODcw.YHHjVA.DoNlv53-mWWPqWPik3Ittvip2gE"
location = " "
isThereLocation = False

@client.event
async def on_ready():
    print ("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content

    if msg.startswith('$test'):
        await message.channel.send("Test")
    if message.content.startswith('$setLocation'):
        location = msg.split("$setLocation ", 1) [1]
        await message.channel.send("Your location is " + location)
        isThereLocation = True
    

client.run(TOKEN)