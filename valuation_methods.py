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
    """
    Calculates the valuation of the company using the discounted cash flow model.
    INPUT:
        cash_and_cash_equivalents: Amount of cash or its equivalents the company is holding right now.
        total_liabilities: The total amount of liability company has at its last announced earnings.
        free_cash_flow: free cash flow is amount of operational money company has minus the amount of capital expenditure required to run everyday business
        shares_outstanding: Number of shares outstanding. The final company's value will be spread to all its shareholders.
        expected_growth_rate_per_annum_in_percentage per annum of the company. Of course this is an estimate, so its better to provide a conservative
            number with some margin of safety
        num_years_forecast of how long this above expected_growth_rate is predicted.

    OUTPUT:
        Per share value of the company, today, using the DCF model
    """
    total_npv_fcf = 0
    for i in range(num_years_forecast):
        #Calculate the free cash flow for the next year
        free_cash_flow = free_cash_flow * cumulative_growth_rate(expected_growth_rate_per_annum_in_percentage, 1)
        #Take the net present value of the fcf
        npv_fcf = net_present_value(free_cash_flow, HISTORIC_MARKET_DISCOUNT_RATE, i + 1)
        total_npv_fcf += npv_fcf
        # Reduce the growth rate of the company, as the company grows older, growth usually declines
        expected_growth_rate_per_annum_in_percentage = apply_margin_of_safety(expected_growth_rate_per_annum_in_percentage, GROWTH_DECLINE_PERCENTAGE)
    #Take the last fcf values npv, and multiply by a constant. This constant represents the company is being sold.
    fcf_value_year_10 = npv_fcf * FCF_MULTIPLIER_YEAR_10
    #Calculate the net company value taking all the npvs of cash, current cash and cash equivalents, and the price of selling. Minus the liabilities
    company_value = total_npv_fcf + fcf_value_year_10 + cash_and_cash_equivalents - total_liabilities
    # Calculate the per share value from the total company value
    per_share_value = company_value / shares_outstanding
    return per_share_value

def roe_valuation(total_shareholders_equity, roe_average_5_years, shares_outstanding, trailing_annual_dividend_rate, expected_growth_rate_per_annum_in_percentage, num_years_forecast):
    """
    Calculates the ROE valuation of the company taking the historic average values and the dividends it pays. 
    Assumptions, company is on average able to maintain its profitability, and gives out some dividends to its shareholders.
    INPUT:
        total_shareholders_equity: Total value of money for all the shareholders equities.
        roe_average_5_years: Last 5 years average return on equity. If the numbers are very different, median should be used. But,
            remember that companies with high volatility's future is also difficult to predict.
        shares_outstanding: Number of shares outstanding
        trailing_annual_dividend_rate: The rate of dividend paid by the company
        expected_growth_rate_per_annum_in_percentage per annum of the company. Of course this is an estimate, so its better to provide a conservative
            number with some margin of safety
        num_years_forecast of how long this above expected_growth_rate is predicted.
    """
    trailing_annual_dividend_rate = trailing_annual_dividend_rate or 0
    #Amount of equity for each share
    shareholders_equity_per_share = total_shareholders_equity / shares_outstanding
    total_npv_dividend = 0
    for i in range(num_years_forecast):
        #Increase equity by the expected growth
        shareholders_equity_per_share = shareholders_equity_per_share * cumulative_growth_rate(expected_growth_rate_per_annum_in_percentage, 1)
        #Increase dividend by expected growth
        trailing_annual_dividend_rate = trailing_annual_dividend_rate * cumulative_growth_rate(expected_growth_rate_per_annum_in_percentage, 1)
        #Take net present value of the dividend
        npv_dividend = net_present_value(trailing_annual_dividend_rate, HISTORIC_MARKET_DISCOUNT_RATE, i)
        total_npv_dividend += npv_dividend
    #Sell the company after the mentioned number of years, so the net income per share is the amount of money each share will be able to generate
    net_income_last_year = shareholders_equity_per_share * roe_average_5_years / 100
    # Required value os the amount of shareholders equity that would be required if company merely earned the historic market returns
    required_value = net_income_last_year / (HISTORIC_MARKET_DISCOUNT_RATE / 100)
    # Take the net present value of that
    npv_required_value = net_present_value(required_value, HISTORIC_MARKET_DISCOUNT_RATE, 10)
    return npv_required_value + total_npv_dividend
