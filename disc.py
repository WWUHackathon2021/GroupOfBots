import discord
import os
import json
import asyncio

client = discord.Client()
TOKEN = "ODMwNDk3Nzc4NTY4Mzk2ODcw.YHHjVA.DoNlv53-mWWPqWPik3Ittvip2gE"
isThereLocation = False
location = " "
priceRange = None

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
        global location
        location = msg.split("$setLocation ", 1) [1]
        await message.channel.send("Your location is " + location)
        isThereLocation = True
    if message.content.startswith('$giveLocation'):
        await message.channel.send("Your location is " + location)

    if message.content.startswith('$setPriceRange'):
        tempAuthor = message.author.id
        await message.channel.send("What price? ($)($$)($$$)($$$$)")
        global priceRange

        def check(m):
            return m.content.startswith('$')
        
        priceRange = await client.wait_for('message', check = check, timeout = 60.0)
        priceRange = priceRange.content

        await message.channel.send("Price Range: " + priceRange)

    if message.content.startswith('$givePriceRange'):
        if(priceRange is not None):
            await message.channel.send("Price Range: " + priceRange)
        else:
            await message.channel.send("No price range selected")
    if message.content.startswith('!setDistance'):
      await message.channel.send("What mile radius would you like (Integer Values Only)")
      global globalDistance

      def check(m):
        return isinstance(int(m.content), int)

      globalDistance = await client.wait_for('message', check = check)
      globalDistance = globalDistance.content
      await message.channel.send("Distance: " + globalDistance + " miles")

client.run(TOKEN)