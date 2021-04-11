from bs4 import BeautifulSoup
import re
from geopy.geocoders import Nominatim
import requests

url = "https://www.yelp.com/search?find_desc=Restaurants&find_loc=Bellingham%2C+WA&ns=1"

soup = BeautifulSoup()

#Search Parameters
#   "location" (of the user) : str
#   "max_dist" : float
#   "dine_in" : bool
#   "take_out" : bool
#   "delivery" : bool
#   "search" : str (the term used to search. Often the quisine. Can be left blank)
#   "min_stars" : float
#   "prince" : int


#Restaurant information Dict
#    "name" : str
#    "rating" : float
#    "price" : int
#    "distance" : float
#    "address" : str
#    "website" : str

class Scraper:
    def __init__(self):
        self._parameters = {}

    def set_parameter(self, parameter, value):
        self._parameters[parameter] = value

    def search(self):
        """Uses the list of parameters to search on yelp for a list of restaurants
        returns a list of dictionaries with restaurants that fit the criteria."""
        
        url = _assemble_yelp_url(self._parameters)
        
        address = _parameters["location"]
        print(coordinates_from_address(address), 5)

        _fetch_html(url)

def coordinates_from_address(address, radius):
    """Given the address and the radius, returns pair of coordinates forming a square that bounds that area"""
    nominatim = Nominatim()
    location = nominatim.geocode(address)
    center = (location.latitude, location.longitude)


def _assemble_yelp_url(parameters):
    """"Uses the dict of parameters to create the necessary yelp url"""
    pass

def _fetch_html(url):
    """Grabs the raw html from the yelp page.
    Returns a list of strings holding chunks of html correspond to the data on restaurants"""
    #sets value for headers
    headers = {"Accept-languag": "en-US, en; q=0.5"}
    # creates empy array to append html chunks to
    restaurant_pages = []
    #Store get reuest to url in variable
    results = requests.get(url, headers=headers)

    restaurant_div = soup.find_all('div', class_='css-1pxmz4g')

    for restaurant in restaurant_div:
        chunk = restaurant.href.a.text
        restaurant_pages.append(chunk)
    return restaurant_pages

def _parse_restaurant(html):
    """Extracts the relvant data from the given html string
    returns a dictionary with the restaurant's information"""
    
    pass

def _check_restaurant(restaurant, parameters):
    """Checks that a restaurant conforms to the search parameters
    Returns true if it does and false if it does not"""
    pass

if __name__ == "__main__":
    print("Testing:")

    scraper = Scraper()

    scraper.search()