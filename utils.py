import requests
from bs4 import BeautifulSoup
from constants import *
import math

def apply_margin_of_safety(value, safety_net_margin_in_percentage):
    return value * (1 - safety_net_margin_in_percentage / 100)

def cumulative_growth_rate(rate_in_percentage, num_years):
    return (1 + rate_in_percentage / 100)**(num_years)

def net_present_value(future_value, rate_in_percentage, num_years):
    return future_value / ((1 + rate_in_percentage / 100)**num_years)

def convert_abbreviated_strings_to_numbers(string):
    abbreviations = {'K': 3, 'M': 6, 'B': 9, 'T': 12}
    return float(string[:-1]) * (10 ** abbreviations[string[-1]])

def scrape_url_to_soup(url):
    try:
        session = requests.Session()
        page = session.get(url)
        return BeautifulSoup(page.content, 'lxml')
    except:
        print ("Cannot read from url = %s"%(url))

def scrape_url_to_jsonsoup(url):
    try:
        session = requests.Session()
        page = session.get(url)
        return BeautifulSoup(page.json()['result'], 'lxml')
    except:
        print ("Cannot read from url = %s"%(url))

def round_values(data):
    return round(data, ROUND_DECIMALS)

def validate_values(data):
    for key in data.keys():
        if math.isnan(data[key]):
            data[key] = 0