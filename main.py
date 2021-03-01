#!/usr/bin/env python

import tickers
from valuation_methods import *
from fetch_tickers import fetch_ticker_data
import time
from constants import *
from tabulate import tabulate
from utils import *
import argparse

def get_valuations(ticker_data):
    return {
        'price_earnings_valuation': price_earnings(ticker_data['earnings_per_share_ttm'],
            ticker_data['historical_price_earnings_ratio_5_years'],
            ticker_data['conservative_growth_rate'],
            5),
        'discounted_cash_flow_valuation': discounted_cash_flow(ticker_data['cash_and_cash_equivalents'],
            ticker_data['total_liabilities'],
            ticker_data['free_cash_flow_ttm'],
            ticker_data['shares_outstanding'],
            ticker_data['conservative_growth_rate'],
            10),
        'roe_valuation': roe_valuation(ticker_data['total_shareholders_equity'],
            ticker_data['roe_average_5_years'],
            ticker_data['shares_outstanding'],
            ticker_data['trailing_annual_dividend_rate'],
            ticker_data['conservative_growth_rate'],
            10)
    }

def prepare_to_print(ticker, ticker_data, valuations):
    return [
        ticker.upper(),
        round_values(ticker_data['current_price']),
        round_values(valuations['price_earnings_valuation']),
        round_values(valuations['discounted_cash_flow_valuation']),
        round_values(valuations['roe_valuation'])
    ]

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--ticker', help = 'Run only for the given ticker')
    namespace, extra_params = args.parse_known_args()

    my_tickers = [namespace.ticker] or tickers.my_tickers

    results = []
    for ticker in my_tickers:
        ticker_data = fetch_ticker_data(ticker)
        if len(ticker_data) > 0:
            valuations = get_valuations(ticker_data)
            results.append(prepare_to_print(ticker, ticker_data, valuations))
        time.sleep(SLEEP_TIME_AFTER_EACH_TICKER)
    print (tabulate(results, headers = [TICKER, CURRENT_PRICE, P_E_VALUATION, DCF_VALUATION, ROE_VALUATION]))
