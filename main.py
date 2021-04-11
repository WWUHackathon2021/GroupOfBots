import discord
import os
from scraper import Scraper

client = discord.Client()
globalDictionary = {
    "address": None,
    "priceRange": None,
    "distance": None,
    "restOption": None,
    "stars": None,
    "cuisine": None,
}


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):

    if message.author == client.user:
        return
    global globalDictionary

    if message.content.startswith("!findRest"):
        globalDictionary["cuisine"] = await getCuisine(message)
        globalDictionary["distance"] = await getDistance(message)
        globalDictionary["address"] = await getAddress(message)
        globalDictionary["priceRange"] = await getPrice(message)
        globalDictionary["stars"] = await getStars(message)
        globalDictionary["restOption"] = await getRestOption(message)
        scraper = scraper_setup()
        await showFood(message, scraper)


def scraper_setup():
    scraper = Scraper()
    restOption = globalDictionary["restOption"]

    scraper.set_parameter("location", globalDictionary["address"])
    scraper.set_parameter("max_dist", float(globalDictionary["distance"]))
    if restOption == 3 or restOption == 4:
        scraper.set_parameter("dine_in", True)
    if restOption == 2 or restOption == 4:
        scraper.set_parameter("take_out", True)
    if restOption == 1 or restOption == 4:
        scraper.set_parameter("delivery", True)
    scraper.set_parameter("description", globalDictionary["cuisine"])
    scraper.set_parameter("min_stars", float(globalDictionary["stars"]))
    scraper.set_parameter("price", len(globalDictionary["priceRange"]))
    return scraper


async def getAddress(message):
    returnAddress = " "
    await message.channel.send("Please enter your address")

    def check(m):
        return m.content.startswith('!')

    returnAddress = await client.wait_for('message', check=check)
    returnAddress = returnAddress.content[1:]
    await message.channel.send("Your address is: " + returnAddress)
    return returnAddress


async def getPrice(message):
    returnPrice = " "
    await message.channel.send(
        "Please enter your price range ($)($$)($$$)($$$$)")

    def check(m):
        return m.content.startswith('!')

    invalid = True
    while invalid:
        returnPrice = await client.wait_for('message', check=check)
        returnPrice = returnPrice.content[1:]
        if returnPrice == "$" or returnPrice == "$$" or returnPrice == "$$$" or returnPrice == "$$$$":
            invalid = False
        else:
            await message.channel.send(
                "Please enter your price range ($)($$)($$$)($$$$)")
    await message.channel.send("Your price range is: " + returnPrice)
    return returnPrice


async def getDistance(message):
    returnDist = " "
    await message.channel.send("Please enter the max distance")

    def check(m):
        return m.content.startswith("!")

    invalid = True
    while invalid:
        returnDist = await client.wait_for('message', check=check)
        returnDist = returnDist.content[1:]
        if returnDist.isnumeric() and float(returnDist) > 0:
            invalid = False
        else:
            await message.channel.send(
                "Please enter a valid number as a distance.")
    await message.channel.send("Your distance is: " + returnDist + " miles")
    return returnDist


async def getRestOption(message):
    returnVal = 0
    await message.channel.send(
        "How do you want to get your food? (1) Delivery, (2) Takeout, (3) Dine-In, (4) Any"
    )

    def check(m):
        return (m.content.startswith("!"))

    invalid = True
    while invalid:
        invalid = False
        returnVal = await client.wait_for('message', check=check)
        returnVal = returnVal.content[1:]
        if returnVal == "1":
            await message.channel.send("You have chosen delivery.")
        elif returnVal == "2":
            await message.channel.send("You have chosen takeout.")
        elif returnVal == "3":
            await message.channel.send("You have chosen dine-In.")
        elif returnVal == "4":
            await message.channel.send("You have chosen any.")
        else:
            invalid = True
            await message.channel.send(
                "Enter a valid number for what kind of restaurant you would like, please. (1) Delivery, (2) Takeout, (3) Dine-In(4) Any"
            )
    return returnVal


async def getStars(message):
    stars = 0
    await message.channel.send("Minimum number of stars? 1-5")
    invalid = True
    while invalid:

        def check(m):
            return (m.content.startswith("!"))

        stars = await client.wait_for('message', check=check)
        stars = stars.content[1:]
        if stars == "1" or stars == "2" or stars == "3" or stars == "4" or stars == "5":
            invalid = False
        else:
            await message.channel.send(
                "Please enter a valid number of stars. 1-5")
    await message.channel.send("Stars: " + stars)
    return stars


async def getCuisine(message):
    returnFood = " "
    await message.channel.send("What kind of food are you hungry for?")

    def check(m):
        return m.content.startswith('!')

    returnFood = await client.wait_for('message', check=check)
    returnFood = returnFood.content[1:]
    await message.channel.send("Food type is: " + returnFood)
    return returnFood


async def showFood(message, scraper):
    foodList = scraper.search()
    foodDict = foodList[0]
    i = 1
    #Finds the highest rated restaurant
    while (i < len(foodList)):
        if (foodDict["rating"] < foodList[i]["rating"]):
            foodDict = foodList[i]
        i += 1

    await message.channel.send("Restaurant: " + foodDict["name"] + "\n" +
                               "Rating :" + foodDict["rating"] + "\n" +
                               "Price: " + foodDict["price"] + "\n" +
                               "Distance: " + foodDict["distance"] + "\n" +
                               "Address: " + foodDict['addresss'] + "\n" +
                               "Website: " + foodDict['website'] + "\n")


client.run(os.getenv('TOKEN'))
