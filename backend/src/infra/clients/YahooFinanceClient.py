import yfinance
from pandas_datareader import data as pdr

yfinance.pdr_override()

CLOSE_KEY = 'Close'

class YahooFinanceClient:
    def get_stocks_data(self, stocks, start_date, end_date):
      data = pdr.get_data_yahoo(stocks, start_date, end_date)
      data = data[CLOSE_KEY]
      returns = data.pct_change()
      means = returns.mean()
      covariance_matrix = returns.cov()
      return means, covariance_matrix
