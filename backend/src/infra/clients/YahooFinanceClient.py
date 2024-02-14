import yfinance
from pandas_datareader import data as pdr

yfinance.pdr_override()

CLOSE_KEY = 'Close'

class YahooFinanceClient:
    def get_daily_returns_as_percentage(self, stocks, start_date, end_date):
      data = pdr.get_data_yahoo(stocks, start_date, end_date)
      data = data[CLOSE_KEY]
      return data.pct_change()
