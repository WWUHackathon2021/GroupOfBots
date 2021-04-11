import discord
import os
import random
from scraper import Scraper
from scraper import verify_address

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

    if message.content.startswith("!FoodBot"):
      await message.channel.send("Hello, I am FoodBot. I will ask you some questions to help you find a place to eat. Start all your responses with a (!)")
      if await set_globals(message) == -1:
        await message.channel.send("Goodbye! Have a nice day.")
        return
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
    if not globalDictionary["cuisine"].lower=="any":
      scraper.set_parameter("description", globalDictionary["cuisine"])
    scraper.set_parameter("min_stars", float(globalDictionary["stars"]))
    scraper.set_parameter("price1", globalDictionary["priceRange"][0])
    scraper.set_parameter("price2", globalDictionary["priceRange"][1])
    scraper.set_parameter("price3", globalDictionary["priceRange"][2])
    scraper.set_parameter("price4", globalDictionary["priceRange"][3])
    return scraper

async def set_globals(message):
  cuis = await getCuisine(message)
  if cuis==-1:
    return-1
  globalDictionary["cuisine"] =cuis

  dis = await getDistance(message)
  if dis==-1:
    return-1
  globalDictionary["distance"] =dis

  adrs = await getAddress(message)
  if adrs==-1:
    return-1
  globalDictionary["address"] =adrs

  price = await getPrice(message)
  if price==-1:
    return-1
  globalDictionary["priceRange"] =price

  stars = await getStars(message)
  if stars==-1:
    return-1
  globalDictionary["stars"] =stars

  opt = await getRestOption(message)
  if opt==-1:
    return-1
  globalDictionary["restOption"] =opt

  return 0


async def getAddress(message):
    returnAddress = " "
    await message.channel.send("What's your address?")

    def check(m):
        return m.content.startswith('!')
    invalid = True
    while invalid:
      returnAddress = await client.wait_for('message', check=check)
      returnAddress = returnAddress.content[1:]
      if returnAddress == "goodbye":
        return-1
      if verify_address(returnAddress):
        invalid = False
      else:
        await message.channel.send("Please enter a valid address.")
    await message.channel.send("Got it. I'll look for places near " + returnAddress)
    return returnAddress


async def getPrice(message):
    price = ""
    returnPrice = [False, False, False, False]
    await message.channel.send(
        "Please list the price ranges you want to look for. (1)$, (2)$$, (3)$$$, (4)$$$")

    def check(m):
        return m.content.startswith('!')

    invalid = True
    while invalid:
        price = await client.wait_for('message', check=check)
        price = price.content[1:]
        if price == "goodbye":
          return -1
        if "1" in price:
          returnPrice[0] = True
          invalid = False
        if "2" in price:
          returnPrice[1] = True
          invalid = False
        if "3" in price:
          returnPrice[2] = True
          invalid = False
        if "4" in price:
          returnPrice[3] = True
          invalid = False
        if invalid:
          await message.channel.send(
                "That doesn't seem like a valid list of prices. Please list the price ranges you want to look for (1)$, (2)$$, (3)$$$, (4)$$$")
    await message.channel.send("Sounds good. I'll look for restaurants with these price ranges: ")
    if returnPrice[0]:
      await message.channel.send("$")
    if returnPrice[1]:
      await message.channel.send("$$")
    if returnPrice[2]:
      await message.channel.send("$$$")
    if returnPrice[3]:
      await message.channel.send("$$$$")
    return returnPrice


async def getDistance(message):
    returnDist = " "
    await message.channel.send("How far away are you willing to go for a restaurant?")

    def check(m):
        return m.content.startswith("!")

    invalid = True
    while invalid:
        returnDist = await client.wait_for('message', check=check)
        returnDist = returnDist.content[1:]
        if returnDist == "goodbye":
          return -1
        if returnDist.isnumeric() and float(returnDist) > 0:
            invalid = False
        else:
            await message.channel.send(
                "Please enter a valid number as a distance.")
    await message.channel.send("Got it! I'll look for restaurants within " + returnDist + " miles.")
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
        if returnVal == "goodbye":
          return -1
        if returnVal == "1":
            await message.channel.send("Alright, I'll look for restaurants that deliver.")
        elif returnVal == "2":
            await message.channel.send("Alright, I'll look for restaurants that offer takeout.")
        elif returnVal == "3":
            await message.channel.send("Alright, I'll just look for any dine-in place.")
        elif returnVal == "4":
            await message.channel.send("Alright, I'll look for any restaurant.")
        else:
            invalid = True
            await message.channel.send(
                "Please enter a valid number for what kind of restaurant you would like. (1) Delivery, (2) Takeout, (3) Dine-In(4) Any"
            )
    return returnVal


async def getStars(message):
    stars = 0
    await message.channel.send("What's the minimum star-rating you want to look for? 1-5")
    invalid = True
    while invalid:

        def check(m):
            return (m.content.startswith("!"))

        stars = await client.wait_for('message', check=check)
        stars = stars.content[1:]
        if stars == "goodbye":
          return -1
        if stars == "1" or stars == "2" or stars == "3" or stars == "4" or stars == "5":
            invalid = False
        else:
            await message.channel.send(
                "Please enter a valid number of stars. 1-5")
    await message.channel.send("I'll look for restaurants with more than " + str(stars) + (" star." if stars==1 else " stars."))
    return stars


async def getCuisine(message):
    returnFood = " "
    await message.channel.send("What kind of food are you hungry for? (Type any if you don't care and want to look for any restaurant.)")

    def check(m):
        return m.content.startswith('!')

    returnFood = await client.wait_for('message', check=check)
    returnFood = returnFood.content[1:]
    if returnFood == "goodbye":
      return -1
    await message.channel.send("Yumm. I'll look for \"" + returnFood + "\" restaurants." )
    return returnFood


async def showFood(message, scraper):
    await message.channel.send("Searching for restaurants...")
    foodList = scraper.search()
    print(foodList)
    leng = len(foodList)
    if leng==0:
      await message.channel.send("There were no restaurants matching your description.")
      return
      
    await message.channel.send(f"There are {leng} restaurants that match your discription. You can either enter (next) to see the next hgihest, or (rand) to see a random one.")

    def check(m):
        return m.content.startswith('!')
    while leng>0:
      request = await client.wait_for('message', check=check)
      request = request.content[1:]
      if request == "goodbye":
        await message.channel.send("Goodbye! I hope you enjoy your food.")
        return
      if request == "next":
        topFood = foodList[0]
        for curRest in foodList:
          if (topFood["rating"] < curRest["rating"]):
            topFood = curRest
        await showRest(message, topFood)
        foodList.remove(topFood)
        leng-=1
      if request == "rand":
        topFood = random.randrange(leng)
        topFood = foodList[topFood]
        await showRest(message, topFood)
        foodList.remove(topFood)
        leng-=1
    await message.channel.send("That's the whole list, you'll have to chose one of those.")
    

async def showRest(message, foodDict):
    price_string = "" if (foodDict["price"] is None) else "Price: " + foodDict["price"]*"$" + "\n"
    await message.channel.send("\nRestaurant: " + str(foodDict["name"]) + "\n" +
                               "Rating :" + str(foodDict["rating"]) + "\n" +
                               price_string +
                               "Website: " + str(foodDict['website']) + "\n")

client.run(os.getenv('TOKEN'))
