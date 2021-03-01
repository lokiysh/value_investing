from utils import *
from constants import *

def price_earnings(earnings_per_share_ttm, historical_price_earnings_ratio, expected_growth_rate_per_annum_in_percentage, num_years_forecast):
    """
    Calculates the estimate current valuation of the company, considering the price-earnings ratios.
    INPUT:
        earnings_per_share_ttm: earnings_per_share_trailing_twelve_months
        historical_price_earnings_ratio of the company such as mean or median of preferrably last 5 years for recency
        expected_growth_rate_per_annum_in_percentage per annum of the company. Of course this is an estimate, so its better to provide a conservative
            number with some margin of safety
        num_years_forecast of how long this above expected_growth_rate is predicted.

    OUTPUT:
        The net present value per share of the company
    """

    #Firstly, we calculate the cumulative growth rate, as the expected growth is per annum, for the number of years we want to forecast
    predicted_growth = cumulative_growth_rate(expected_growth_rate_per_annum_in_percentage, num_years_forecast)
    #Next we can calculate the future price of the share as EPS * P/E(historic) * growth
    future_predicted_price = earnings_per_share_ttm * historical_price_earnings_ratio * predicted_growth
    #Finally, we scale back the future price to the present day value, taking the historic market discount rate.
    return net_present_value(future_predicted_price, HISTORIC_MARKET_DISCOUNT_RATE, num_years_forecast)

def discounted_cash_flow(cash_and_cash_equivalents, total_liabilities, free_cash_flow, shares_outstanding, expected_growth_rate_per_annum_in_percentage, num_years_forecast):
    total_npv_fcf = 0
    for i in range(num_years_forecast):
        free_cash_flow = free_cash_flow * cumulative_growth_rate(expected_growth_rate_per_annum_in_percentage, 1)
        npv_fcf = net_present_value(free_cash_flow, HISTORIC_MARKET_DISCOUNT_RATE, i + 1)
        total_npv_fcf += npv_fcf
        expected_growth_rate_per_annum_in_percentage = apply_margin_of_safety(expected_growth_rate_per_annum_in_percentage, GROWTH_DECLINE_PERCENTAGE)
    fcf_value_year_10 = npv_fcf * FCF_MULTIPLIER_YEAR_10
    company_value = total_npv_fcf + fcf_value_year_10 + cash_and_cash_equivalents - total_liabilities
    per_share_value = company_value / shares_outstanding
    return per_share_value

def roe_valuation(total_shareholders_equity, roe_average_5_years, shares_outstanding, trailing_annual_dividend_rate, expected_growth_rate_per_annum_in_percentage, num_years_forecast):
    trailing_annual_dividend_rate = trailing_annual_dividend_rate or 0
    shareholders_equity_per_share = total_shareholders_equity / shares_outstanding
    total_npv_dividend = 0
    for i in range(num_years_forecast):
        shareholders_equity_per_share = shareholders_equity_per_share * cumulative_growth_rate(expected_growth_rate_per_annum_in_percentage, 1)
        trailing_annual_dividend_rate = trailing_annual_dividend_rate * cumulative_growth_rate(expected_growth_rate_per_annum_in_percentage, 1)
        npv_dividend = net_present_value(trailing_annual_dividend_rate, HISTORIC_MARKET_DISCOUNT_RATE, i)
        total_npv_dividend += npv_dividend
    net_income_last_year = shareholders_equity_per_share * roe_average_5_years / 100
    required_value = net_income_last_year / (HISTORIC_MARKET_DISCOUNT_RATE / 100)
    npv_required_value = net_present_value(required_value, HISTORIC_MARKET_DISCOUNT_RATE, 10)
    return npv_required_value + total_npv_dividend
