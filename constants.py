SAFETY_MARGIN_PERCENTAGE = 25 #Since predicting the future is not perfect, we reduce the future growth numbers by this percentage
HISTORIC_MARKET_DISCOUNT_RATE = 9 # Historic return averages of the market
GROWTH_DECLINE_PERCENTAGE = 5 # As company grows, it growth percentage should decline by this amount in percentage
FCF_MULTIPLIER_YEAR_10 = 12 # If company is sold after 10 years, the multiplies for the free cash flow, usually in the range[10-15]
SLEEP_TIME_AFTER_EACH_TICKER = 3 # Sleeps for given number of seconds after processing each ticker
ROUND_DECIMALS = 2 #Rounds values to given decimal place, 14.234213 = 14.23

#Constants for pretty print
TICKER = "Ticker"
CURRENT_PRICE = "Current Price"
P_E_VALUATION = "P/E Valuation"
DCF_VALUATION = "DCF Valuation"
ROE_VALUATION = "ROE Valuation"
EX_DIVIDEND_DATE = 'EX Dividend date'
DAYS_TO_DIVIDEND = 'Days to Dividend'
EXPECTED_DIVIDEND = 'Expected Dividend'
