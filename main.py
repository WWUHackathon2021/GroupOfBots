import discord
import os
import json
import asyncio

client = discord.Client()
TOKEN = "ODMwNDk3Nzc4NTY4Mzk2ODcw.YHHjVA.DoNlv53-mWWPqWPik3Ittvip2gE"
isThereLocation = False
location = " "
priceRange = None
globalDistance = 0
restOption = 0
stars = 0
globalDictionary = {
 "state" : None,
 "city" : None,
 "priceRange" : None,
 "distance" : None,
 "restOption" : None,
 "stars" : None,
}

@client.event
async def on_ready():
    print ("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    msg = message.content
    global globalDictionary
    
    if msg.startswith("!findRest"):
        globalDictionary["state"] = await getState(message)
        globalDictionary["city"] = await getCity(message)
        globalDictionary["priceRange"] = await getPrice(message)
        globalDictionary["distance"] = await getDistance(message)
        globalDictionary["restOption"] = await getRestOption(message)
        globalDictionary["stars"] = await getStars(message)
        await message.channel.send(globalDictionary)
    
async def getState(message):
    returnState = " "
    await message.channel.send("Please enter your state")
    def check(m):
        return len(m.content) == 2
    returnState = await client.wait_for('message', check = check)
    returnState = returnState.content
    await message.channel.send("Your state is: " + returnState)
    return returnState
            
async def getCity(message):
    returnCity = " "
    await message.channel.send("Please enter your city")
    def check(m):
        return m
    returnCity = await client.wait_for('message', check = check)
    returnCity = returnCity.content
    await message.channel.send("Your city is: " + returnCity)
    return returnCity
async def getPrice(message):
    returnPrice = " "
    await message.channel.send("Please enter your price range ($)($$)($$$)($$$$)")
    def check(m):
        return m.content.startswith('$')
    returnPrice = await client.wait_for('message', check = check)
    returnPrice = returnPrice.content
    await message.channel.send("Your price range is: " + returnPrice)
    return returnPrice
async def getDistance(message):
    returnDist = " "
    await message.channel.send("Please enter the max distance")
    def check(m):
        return m.content.isnumeric
    returnDist = await client.wait_for('message', check = check)
    returnDist = returnDist.content
    await message.channel.send("Your distance is: " + returnDist + " miles")
    return returnDist
async def getRestOption(message):
    returnVal = 0
    await message.channel.send("How do you want to get your food? (1) Delivery, (2) Takeout, (3) Dine-In, (4) Any")
    def check(m):
        return(int (m.content) in range(1,5))
    returnVal = await client.wait_for('message', check = check)
    returnVal = returnVal.content
    await message.channel.send(returnVal)
    return returnVal
async def getStars(message):
    stars = 0
    await message.channel.send("Minimum number of stars? 1-5")
    def check(m):
        return (int (m.content) in range(1,6))
    stars = await client.wait_for('message', check = check)
    stars = stars.content
    await message.channel.send("Stars: " + stars)
    return stars



client.run(TOKEN)