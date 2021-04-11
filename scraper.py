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
#   "price" : int


#Restaurant information Dict
#    "name" : str
#    "rating" : float
#    "price" : int
#    "distance" : float
#    "address" : str
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
            "price"       : int}

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
        
        pass

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
    attributes = "&attrs=" if (take_out or delivery) else ""  
    attributes += "RestaurantsDelivery" if delivery else ""
    attributes += "%2C" if (take_out and delivery) else ""
    attributes += "RestaurantsTakeOut" if take_out else ""

    #Price Range
    price = parameters.get("price", 0)
    attributes += "%2C" if (take_out or delivery) else ""
    attributes += f"RestaurantsPriceRange2.{price}" if price!=0 else ""

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

def _parse_restaurant(html):
    """Extracts the relvant data from the given html string
    returns a dictionary with the restaurant's information"""
    
    pass

def _check_restaurant(restaurant, parameters):
    """Checks that a restaurant conforms to the search parameters
    Returns true if it does and false if it does not"""
    if(restaurant["distance"] > parameters["max_distance"]): return False
    if(restaurant["rating"] < parameters["min_stars"]): return False
    if(restaurant["price"] > parameters["price"]): return False
    else: return True

if __name__ == "__main__":
    print("Testing:")

    scraper = Scraper()
    
    scraper.set_parameter("location", "1232 235th PL SW")
    scraper.set_parameter("max_dist", 5.0)
    scraper.set_parameter("take_out", True)
    scraper.set_parameter("description", "Thai Food")
    scraper.set_parameter("price", 2)

    url = _assemble_yelp_url(scraper._parameters)

    print(url)

    pages = _fetch_html(url)

    print(pages)
    