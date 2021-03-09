#!/usr/bin/env python

from yahoo_fin.stock_info import *
import tickers
import argparse
import datetime
from tabulate import tabulate
from constants import *
import time
from utils import *

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--ticker', help = 'Run only for the given ticker')
    namespace, extra_params = args.parse_known_args()

    #If there is --ticker argument, use that, otherwise read the entire list of tickers in tickers.py
    my_tickers = tickers.dividend_tickers
    if (namespace.ticker):
        my_tickers = [namespace.ticker]

    result = []
    for ticker in my_tickers:
        try:
            stats_info = get_stats(ticker)
            stats_info = dict(zip(stats_info['Attribute'], stats_info['Value']))
            ex_dividend_date = stats_info['Ex-Dividend Date 4']
            forward_annual_dividend_rate = float(stats_info['Forward Annual Dividend Rate 4'])
            quaterly_expected_dividend = round_values(forward_annual_dividend_rate / 4)
            days_from_today = (datetime.datetime.strptime(ex_dividend_date, '%b %d, %Y') - datetime.datetime.today()).days
            if days_from_today >= 0:
                result.append([ticker.upper(), ex_dividend_date, days_from_today, quaterly_expected_dividend])
        except:
            print ("Cannot read stats info for %s"%(ticker))
        time.sleep(SLEEP_TIME_AFTER_EACH_TICKER)
    result.sort(key = lambda x : x[2])
    print (tabulate(result, headers = [TICKER, EX_DIVIDEND_DATE, DAYS_TO_DIVIDEND, EXPECTED_DIVIDEND]))