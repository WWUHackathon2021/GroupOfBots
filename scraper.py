from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import requests
import re, math

url = "https://www.yelp.com/search?find_desc=Restaurants&find_loc=Bellingham%2C+WA&ns=1"



#Search Parameters
#   "location" (of the user) : str
#   "max_dist" : float
#   "dine_in" : bool
#   "take_out" : bool
#   "delivery" : bool
#   "description" : str (the term used to search. Often the cuisine. Can be left blank)
#   "min_stars" : float
#   "price1" : bool
#   "price2" : bool
#   "price3" : bool
#   "price4" : bool


#Restaurant information Dict
#    "name" : str
#    "rating" : float
#    "price" : int
#    "website" : str



MPD_AT_EQUATOR = 69 #Miles per degree at the equator

PARAMETER_TYPE_DICT = {
            "location"    : str,
            "max_dist"    : float,
            "dine_in"     : bool,
            "take_out"    : bool,
            "delivery"    : bool,
            "description" : str,
            "min_stars"   : float,
            "price1"       : bool,
            "price2"       : bool,
            "price3"       : bool,
            "price4"       : bool,}

class ParameterException(Exception):
    pass

class Scraper:
    def __init__(self):
        self._parameters = {}


    def set_parameter(self, parameter, value):
        if parameter not in PARAMETER_TYPE_DICT.keys():
            raise ParameterException(f"\"{parameter}\" is not a recongized parameter name")
        
        elif PARAMETER_TYPE_DICT[parameter] != type(value):
            raise ParameterException(f"\"{parameter}\" is expected to be {PARAMETER_TYPE_DICT[parameter]}, not  {type(value)}")
        else:
            self._parameters[parameter] = value

    def search(self):
        """Uses the list of parameters to search on yelp for a list of restaurants
           returns a list of dictionaries with restaurants that fit the criteria."""
        
        url = _assemble_yelp_url(self._parameters)
        print(url)
        chunks = _fetch_html(url)

        restaurants = [_parse_restaurant(chunk) for chunk in chunks]

        checked_restaurants = []
        for restaurant in restaurants:
          if _check_restaurant(restaurant, self._parameters):
            checked_restaurants.append(restaurant)

        return checked_restaurants

def coordinates_from_address(address, radius):
    """Given the address and the radius, returns a 4-tuple of two sets of coordinates forming a square that bounds that area
       The coordinites are ordered (longitude, latitude) and the coordinates are ordered (southwest point, northeast point)"""
    nominatim = Nominatim(user_agent = "Restaurant-Bot")
    location = nominatim.geocode(address)
    
    eastward_displacement =  miles_to_longitude(radius/2, location.latitude)
    northward_displacement = miles_to_latitude(radius/2)

    ne_point = (location.latitude + northward_displacement, location.longitude + eastward_displacement)
    sw_point = (location.latitude - northward_displacement, location.longitude - eastward_displacement)

    return sw_point[1], sw_point[0], ne_point[1], ne_point[0]

def _assemble_yelp_url(parameters):
    """"Uses the dict of parameters to create the necessary yelp url"""

    #Description
    description =  "find_desc=" + parameters.get("description", "")
    
    #Address
    address = parameters.get("location", "")
    find_loc = f"&find_loc={address}"

    #Location
    max_dist = parameters.get("max_dist", 0)
    coordinates = coordinates_from_address(address, max_dist)
    location = f"&l=g%3A{coordinates[0]}%2C{coordinates[1]}%2C{coordinates[2]}%2C{coordinates[3]}" if max_dist else ""

    #Take Out / Delivery
    take_out = parameters.get("take_out", False)
    delivery = parameters.get("delivery", False)
    attributes = "&attrs="
    attributes += "RestaurantsDelivery" if delivery else ""
    attributes += "%2C" if (take_out and delivery) else ""
    attributes += "RestaurantsTakeOut" if take_out else ""

    #Price Range
    attributes += "%2C" if (take_out or delivery) else ""
    
    price1 = parameters.get("price1", False)
    attributes += f"%2CRestaurantsPriceRange2.1" if price1 else ""

    price2 = parameters.get("price2", False)
    attributes += f"%2CRestaurantsPriceRange2.2" if price2 else ""

    price3 = parameters.get("price3", False)
    attributes += f"%2CRestaurantsPriceRange2.3" if price3 else ""

    price4 = parameters.get("price4", False)
    attributes += f"%2CRestaurantsPriceRange2.4" if price4 else ""

    url = f"https://www.yelp.com/search?{description}{find_loc}{location}{attributes}&sortby=rating"

    fixed_url = []

    for i, char in enumerate(url):
        if char == " " : fixed_url.append("%20")
        elif char == "," : fixed_url.append("%2C")
        else: fixed_url.append(char)
    
    return "".join(fixed_url)


def miles_to_longitude(miles, latitude):
    miles_per_degree = math.cos(latitude * (math.pi/180)) * MPD_AT_EQUATOR
    return miles / miles_per_degree

def miles_to_latitude(miles):
    return miles / MPD_AT_EQUATOR

def _fetch_html(url):
    """Grabs the raw html from the yelp page.
    Returns a list of strings holding chunks of html correspond to the data on restaurants"""
    
    #check if business name has number to avoid ads
    #https://www.yelp.com/search?find_desc=Thai%20Food&find_loc=Bellingham%2C%20WA (page 1)
    #https://www.yelp.com/search?find_desc=Thai%20Food&find_loc=Bellingham%2C%20WA&start=10

    #sets value for headers
    headers = {"Accept-languag": "en-US, en; q=0.5"}
    # creates empy array to append html chunks to
    restaurant_chunks = []
    #Store get reuest to url in variable
    results = requests.get(url, headers=headers)

    soup = BeautifulSoup(results.text, "html.parser")
    restaurants = soup.find_all("div", "businessName__09f24__3Wql2 display--inline-block__09f24__3L1EB border-color--default__09f24__1eOdn")

    for restaurant in restaurants:
        restaurant_chunks.append(list(restaurant.parents)[5])
    
    return restaurant_chunks

def _parse_restaurant(restaurant):
    """Extracts the relvant data from the given html string
    returns a dictionary with the restaurant's information"""
    

    a_tag = restaurant.find("a", class_="css-166la90")
    rating_img = restaurant.find("img", src="https://s3-media0.fl.yelpcdn.com/assets/public/stars_v2.yji-52d3d7a328db670d4402843cbddeed89.png")
    rating_div = rating_img.find_parent()
    price_span = restaurant.find("span", class_="priceRange__09f24__2O6le css-xtpg8e")


    name = a_tag.get_text()

    rating = rating_div.get("aria-label")
    rating = float(rating.split(" ")[0])
    
    price = price_span.get_text()
    price = len(price)

    website =  "https://www.yelp.com" + str(a_tag.get("href"))

    restaurant_dict = {}
    restaurant_dict["name"] = name
    restaurant_dict["rating"] = rating
    restaurant_dict["price"] = price
    restaurant_dict["website"] = website

    return restaurant_dict



def _check_restaurant(restaurant, parameters):
    """Checks that a restaurant conforms to the search parameters
    Returns true if it does and false if it does not"""
    if(restaurant["rating"] < parameters["min_stars"]): return False
    if(restaurant["price"] > parameters["price"]): return False
    else: return True

if __name__ == "__main__":
    print("Testing:")

    scraper = Scraper()
    
    scraper.set_parameter("location", "516 High St. Bellingham, WA")
    scraper.set_parameter("max_dist", 15.0)
    scraper.set_parameter("take_out", True)
    scraper.set_parameter("delivery", True)
    scraper.set_parameter("dine_in", True)
    scraper.set_parameter("description", "Pizza")
    scraper.set_parameter("price", 3)

    url = _assemble_yelp_url(scraper._parameters)

    print(url)

    chunks = _fetch_html(url)

    for chunk in chunks:
        print(_parse_restaurant(chunk))
        
    