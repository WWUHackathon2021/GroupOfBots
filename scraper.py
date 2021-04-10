from bs4 import BeautifulSoup


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
        
        pass

def _assemble_yelp_url(parameters):
    """"Uses the dict of parameters to create the necessary yelp url"""
    pass

def _fetch_html(url):
    """Grabs the raw html from the yelp page.
    Returns a list of strings holding chunks of html correspond to the data on restaurants"""
    
    pass

def _parse_restaurant(html):
    """Extracts the relvant data from the given html string
    returns a dictionary with the restaurant's information"""
    
    pass

def _check_restaurant(restaurant, parameters):
    pass

if __name__ == "__main__":
    print("Testing:")