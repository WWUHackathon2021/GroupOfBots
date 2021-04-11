import discord
import os
import json
import asyncio

client = discord.Client()
TOKEN = "ODMwNDk3Nzc4NTY4Mzk2ODcw.YHHjVA.DoNlv53-mWWPqWPik3Ittvip2gE"
sThereLocation = False
location = " "
priceRange = None
globalDistance = 0
restOption = 0
stars = 0


@client.event
async def on_ready():
    print ("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    msg = message.content

    if msg.startswith('!test'):
        sayHi()
    if message.content.startswith('!setLocation'):
        global location
        location = msg.split("!setLocation ", 1) [1]
        await message.channel.send("Your location is " + location)
        isThereLocation = True
    if message.content.startswith('!giveLocation'):
        if(isThereLocation):
          await message.channel.send("Your location is " + location)
        else:
          await message.channel.send("You haven't set your location yet")

    if message.content.startswith('!setPriceRange'):
        await message.channel.send("What price? ($)($$)($$$)($$$$)")
        global priceRange

        def check(m):
            return m.content.startswith('$')
        
        priceRange = await client.wait_for('message', check = check, timeout = 60.0)
        priceRange = priceRange.content

        await message.channel.send("Price Range: " + priceRange)

    if message.content.startswith('!givePriceRange'):
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

    if message.content.startswith("!restaurantType"):
        i = 1
        while(i != 0):
            await message.channel.send("What type of restaurant would you like (1) Take-Out (2) Dine-in (3) Delivery (4) Any")
            global restOption

            def check(m):
                return m.content
        
            restOption = await client.wait_for('message', check = check)
            restOption = restOption.content
            if(int(restOption) in range (1,4)):
                await message.channel.send("Option: " + restOption)
                i = 0
            else:
                await message.channel.send("Please select a valid option")

    if message.content.startswith("!setStars"):
        i = 1
        while(i != 0):
            await message.channel.send("How many stars should the restaraunt have?")
            global stats
        
            def check(m):
                return m.content
            stars = await client.wait_for('message', check = check)
            stars = stars.content
            if(int(stars) in range(1,5)):
                await message.channel.send("Stars: " + ('*') * int(stars))
                i = 0
            else:
                await message.channel.send("Please select a valid option (Int between 1 and 5)")

@client.event
async def sayHi():
  return "heelo user"

client.run(TOKEN)

