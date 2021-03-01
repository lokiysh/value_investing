from yahoo_fin.stock_info import *
from utils import *
from constants import *

def fetch_ticker_data(ticker):
    """
    Fetches all the required data for the given ticker from multiple sources (yahoo finances, and morningstar.com)
    Returned data structure has the following fields:
    {
        total_liabilities,
        total_shareholders_equity,
        expected_growth_rate_future_in_percentage_5_years,
        conservative_growth_rate,
        earnings_per_share_ttm,
        trailing_annual_dividend_rate,
        shares_outstanding,
        current_price,
        historical_price_earnings_ratio_5_years,
        roe_average_5_years,
        cash_and_cash_equivalents,
        free_cash_flow_ttm
    }

    It calls various private methods below to fulfill this information.
    Companies which are less than 5 years old have the historical_price_earnings_ratio_5_years as 0 and roe_average_5_years computed since its epoch.

    Finally it also validates the values to get rid of nans for the above cases.
    """
    ticker_data = {}
    _get_return_of_equity_historic_average(ticker, ticker_data)
    _get_balance_sheet_info(ticker, ticker_data)
    _get_historical_price_earning_ratio(ticker, ticker_data)
    _get_growth_rate(ticker, ticker_data)
    _get_stats(ticker, ticker_data)
    _get_free_cash_flow(ticker, ticker_data)
    _get_live_price(ticker, ticker_data)
    _get_cash_and_cash_equivalents(ticker, ticker_data)
    validate_values(ticker_data)
    return ticker_data

def _get_balance_sheet_info(ticker, ticker_data):
    try:
        balance_sheet_info = get_balance_sheet(ticker)
        balance_sheet_info = balance_sheet_info[balance_sheet_info.columns[0]]
        ticker_data['total_liabilities'] = float(balance_sheet_info['totalLiab'])
        ticker_data['total_shareholders_equity'] = float(balance_sheet_info['totalStockholderEquity'])
    except:
        print ("Cannot read balance sheet info for %s"%(ticker))

def _get_growth_rate(ticker, ticker_data):
    try:
        analysts_info = get_analysts_info(ticker)
        growth_rate_next_5_years_string = analysts_info['Growth Estimates'][ticker][4]
        ticker_data['expected_growth_rate_future_in_percentage_5_years'] = float(growth_rate_next_5_years_string[:-1])
        ticker_data['conservative_growth_rate'] = apply_margin_of_safety(ticker_data['expected_growth_rate_future_in_percentage_5_years'], SAFETY_MARGIN_PERCENTAGE)
    except:
        print ("Cannot read analysts info for %s"%(ticker))

def _get_stats(ticker, ticker_data):
    try:
        stats_info = get_stats(ticker)
        stats_info = dict(zip(stats_info['Attribute'], stats_info['Value']))
        ticker_data['earnings_per_share_ttm'] = float(stats_info['Diluted EPS (ttm)'])
        ticker_data['trailing_annual_dividend_rate'] = float(stats_info['Trailing Annual Dividend Rate 3'])
        ticker_data['shares_outstanding'] = convert_abbreviated_strings_to_numbers(stats_info['Shares Outstanding 5'])
    except:
        print ("Cannot read stats info for %s"%(ticker))

def _get_live_price(ticker, ticker_data):
    try:
        live_price = get_live_price(ticker)
        ticker_data['current_price'] = float(live_price)
    except:
        print ("Cannot read live price for %s"%(ticker))

def _get_historical_price_earning_ratio(ticker, ticker_data):
    try:
        url = 'http://financials.morningstar.com/valuate/current-valuation-list.action?t=' + ticker
        soup = scrape_url_to_soup(url)
        price_earnings_tag = soup.find(lambda tag:tag.name == 'th' and 'Price/Earnings' in tag.text)
        historic_price_earning_ratio = price_earnings_tag.parent.find_all('td')[3].text
        ticker_data['historical_price_earnings_ratio_5_years'] = float(historic_price_earning_ratio) if historic_price_earning_ratio  != '—' else 0
    except:
        print ("Cannot read historic_price_earning_ratio for ticker %s"%(ticker))

def _get_free_cash_flow(ticker, ticker_data):
    try:
        url = 'http://financials.morningstar.com/finan/financials/getFinancePart.html?t=' + ticker
        soup = scrape_url_to_soup(url)
        free_cash_flow_tag = soup.find(lambda tag:tag.name == 'th' and 'Free Cash Flow' in tag.text)
        free_cash_flow_text = free_cash_flow_tag.parent.find_all('td')[10].text.replace(",", "")
        ticker_data['free_cash_flow_ttm'] = float(free_cash_flow_text) * (10**6)
    except:
        print ("Cannot read free_cash_flow_ttm for ticker %s"%(ticker))

def _get_cash_and_cash_equivalents(ticker, ticker_data):
    try:
        url = 'http://financials.morningstar.com/ajax/ReportProcess4HtmlAjax.html?reportType=bs&t=' + ticker
        soup = scrape_url_to_jsonsoup(url)
        cash_and_cash_equivalent_tag = soup.find(id = 'data_i1')
        current_year_cash = cash_and_cash_equivalent_tag.find(id = 'Y_5')
        ticker_data['cash_and_cash_equivalents'] = float(current_year_cash['rawvalue'])
    except:
        print ("Cannot read cash and cash equivalent for ticker %s"%(ticker))

def _get_return_of_equity_historic_average(ticker, ticker_data):
    try:
        url = 'http://financials.morningstar.com/finan/financials/getKeyStatPart.html?t=' + ticker
        soup = scrape_url_to_soup(url)
        roe_tag = soup.find(lambda tag:tag.name == 'th' and 'Return on Equity %' in tag.text)
        roe_historic = roe_tag.parent.find_all('td')
        roe_last_5_years = []
        for i in range(len(roe_historic) - 6, len(roe_historic) - 1):
            if roe_historic[i].text != '—':
                roe_last_5_years.append(float(roe_historic[i].text))
        ticker_data['roe_average_5_years'] = sum(roe_last_5_years) / len(roe_last_5_years)
    except:
        print ("Cannot read ROE for ticker %s"%(ticker))