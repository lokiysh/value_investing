## Estimating Intrinsic Values of Companies

This project can be used for calculating an estimation of instrinsic values of companies. This could be useful for long term investments in stocks, but by no means, should be treated as any piece of financial advice by itself. Please use your own judgement before investing. There are multiple methods used to estimate the valuation of tickers, and the code automatically pulls up the relevant data from its sources, [finance.yahoo.com](finance.yahoo.com)  and [financials.morningstar.com](financials.morningstar.com).


### Installation

This project is still in its beta testing phase. So for now, you need to clone the repository and install dependencies yourself. Later, I will move it to a standalone package.

1. git clone git@github.com:lokiysh/value_investing.git
2. Install [Python 3](https://www.python.org/downloads/)
3. pip install yahoo_fin
4. pip install tabulate
5. pip install requests
6. pip install beautifulsoup4

### Run

To run the project, go to the source directory where you cloned the project and run `python3 main.py --ticker=AAPL`. You can of course change the ticker to your liking. If you have multiple tickers, you can edit the file `tickers.py` and all your instruments there, and then run without the `--ticker` argument.
![Samples](/sample.png)

### Models

#### Price-Earnings (P/E) Model

In this model we take the 5 year historic P/E valuation (such as an average) and then use the predicted growth numbers to forecast the future values. If the trailing twelve months earnings-per-share of the company is denoted by `EPS(TTM)` and the average historic price-earnings for last 5 years as `P/E`, and the expected growth rate of the company for the next 5 years as `Growth 5 Years (per annum)`, then we can compute the future price as `EPS(TTM) * P/E * Growth 5 Years (per annum)`. Since the growth rates are estimates of analysts, in this project we take a safety net and cut it down by 25%. You can change this number at `constants.py` if, for example, you want to be more aggressive.

Once we get the price per stock of the company in future, we want to bring it back to the present day net value, because that is the value which will tell us what the intrinsic value of the company is today. To achieve that, we will use a discount rate of 9%, which is approximately equal to the long term historical return of the stock market. This is the minimum rate of return you would have to earn to justify picking the stock over an index fund, for example. So, our Net Present Value (NPV) of the stock becomes, `future_price / (1.09)^5`. Again, you can change the discount rate if you wish to in constants.py.

#### Discounted Cash Flow (DCF) Model

In this model, we add up all the future cash the company can generate, and take the net present value of the company. We assume the company is sold after 10 years, and use that cash reserves to determine the net value of the company. 
"*[Intrinsic value is] the discounted value of the cash that can be taken out of a business during its remaining life." ~ Warren Buffett in Berkshire Hathaway Owner Manual*

We take the Free Cash Flow (FCF) of the last 12 months, and then project it in the future with the company's growth rate. It is important to note that we are not taking the operating cash flow, but FCF. Cash for operating activities is the cash generated from company's normal operations. However, we cannot take all the money out because we still want the business to be running, so we reduce from this the CAPEX or Capital Expenditure for everyday business run, and get FCF in the end.

So we take up FCF for last 12 months, and project it 10 years into the future with an anticipated growth rate per annum of the company. It then takes the NPV of these cash flows and add them up. We also add the cash and cash equivalents (company might be having some other form of cash reserves with them), and subtract all the debt the company. Also we can assume the company is sold after 10 years. and multiply the last year FCF by a multiple to denote this. This value, is usually between 10-15, and is rather arbitrary, and we have chosen it to be 12 to be on the conservative side.

Finally, we have the net value of the company, we can divide this value between all share holders, and we have the intrinsic value of the company based on cash only reserves.

#### Return on Equity (ROE) Model

Return on Equity is simply the net income of the company divided by the shareholders equity. Higher, the better, it means the company is more profitable. Since dividends also count in ROE and we have no way to predict them, we assume that the company is going to pay out the same percentage of its profits as dividends in the future. In this model, we take the last 5 years historic ROE's median. If the company is new and does not have 5 years of data, we simply take the ROE (ttm). We take the total shareholder equity and divide by the number of shares. We let it grow for 10 years with the growth rate predicted for the company (again, like in P/E we take a conservative approach and reduce it by 25%).

We do the same for the dividends values, and let it grow by this conservative growth rate. In the end we will take the NPV of those dividends at the market discount rate. Year 10 net income per share is the amount which each shareholder equity will earn on yeat 10, so we multiply the shareholder equity per share with ROE. To calculate how much should be this value so that company just earns the equality of market returns (9%), we divide the last year net income with 0.09. Finally we can take the NPV of this value and add the sum of NPV dividends to see our net returns. This will determine the intrinsic value of the company based on ROEs.

