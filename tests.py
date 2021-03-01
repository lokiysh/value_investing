import unittest
from valuation_methods import *

class TestValuationMethods(unittest.TestCase):

    aapl_ticker_data = {
        'earnings_per_share_ttm': 11.89,
        'historical_price_earnings_ratio_5_years': 15.4,
        'expected_growth_rate_future_in_percentage_5_years': 9.86,
        'free_cash_flow_ttm': 58245000000,
        'cash_and_cash_equivalents': 48844000000,
        'total_liabilities': 248028000000,
        'shares_outstanding': 4520000000,
        'roe_average_5_years': 45.06,
        'total_shareholders_equity': 90488000000,
        'trailing_annual_dividend_rate': 3.00,
        'conservative_growth_rate': 7.395
    }

    def test_price_earnings(self):
        price_earnings_valuation = price_earnings(self.aapl_ticker_data['earnings_per_share_ttm'],
            self.aapl_ticker_data['historical_price_earnings_ratio_5_years'],
            self.aapl_ticker_data['conservative_growth_rate'],
            5)
        self.assertEqual(round(price_earnings_valuation, 2), 170.02)

    def test_discounted_cash_flow(self):
        dcf_valuation = discounted_cash_flow(self.aapl_ticker_data['cash_and_cash_equivalents'],
            self.aapl_ticker_data['total_liabilities'],
            self.aapl_ticker_data['free_cash_flow_ttm'],
            self.aapl_ticker_data['shares_outstanding'],
            self.aapl_ticker_data['conservative_growth_rate'],
            10)
        self.assertEqual(round(dcf_valuation, 2), 185.34)

    def test_roe_valuation(self):
        roe_valuations = roe_valuation(self.aapl_ticker_data['total_shareholders_equity'],
            self.aapl_ticker_data['roe_average_5_years'],
            self.aapl_ticker_data['shares_outstanding'],
            self.aapl_ticker_data['trailing_annual_dividend_rate'],
            self.aapl_ticker_data['conservative_growth_rate'],
            10)

        self.assertEqual(round(roe_valuations, 2), 116.58)



if __name__ == '__main__':
    unittest.main()