import requests
from bs4 import BeautifulSoup
from constants import *
import math

def apply_margin_of_safety(value, safety_net_margin_in_percentage):
    """
    Takes a value, and reduces it by a safety margin given
    """
    return value * (1 - safety_net_margin_in_percentage / 100)

def cumulative_growth_rate(rate_in_percentage, num_years):
    """
    Increases the rate cumulatively over a given number of years
    """
    return (1 + rate_in_percentage / 100)**(num_years)

def net_present_value(future_value, rate_in_percentage, num_years):
    """
    Finds the net present value for a future value. Usually rate_in_percentage is the HISTORIC_MARKET_DISCOUNT_RATE 
    """
    return future_value / ((1 + rate_in_percentage / 100)**num_years)

def convert_abbreviated_strings_to_numbers(string):
    """
    Converts abbreivated string amounts to numbers, such as 1.2M = 1200000 and 14K = 14000
    """
    abbreviations = {'K': 3, 'M': 6, 'B': 9, 'T': 12}
    return float(string[:-1]) * (10 ** abbreviations[string[-1]])

def scrape_url_to_soup(url):
    """
    Scrapes the given url page and returns a beautifulSoup object of it
    """
    try:
        session = requests.Session()
        page = session.get(url)
        return BeautifulSoup(page.content, 'lxml')
    except:
        print ("Cannot read from url = %s"%(url))

def scrape_url_to_jsonsoup(url):
    """
    Scrapes the given url page which has a json response and returns a beautifulSoup object of it
    """
    try:
        session = requests.Session()
        page = session.get(url)
        return BeautifulSoup(page.json()['result'], 'lxml')
    except:
        print ("Cannot read from url = %s"%(url))

def round_values(data):
    """
    Rounds the given decimal values to ROUND_DECIMALS (defined in constants as 2) places
    """
    return round(data, ROUND_DECIMALS)

def validate_values(data):
    """
    Validates all the numbers in the data dictionary. If any of them is nan, it is replaced to 0.
    """
    for key in data.keys():
        if math.isnan(data[key]):
            data[key] = 0