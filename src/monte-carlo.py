import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
from datetime import datetime, timedelta
import yfinance

CLOSE_KEY = 'Close'
SAMPLE_NUMBER_OF_DAYS = 300
NUMBER_OF_DAYS = 100
NUMBER_OF_SIMS = 10000
INITIAL_PORTFOLIO_VALUE = 10000

yfinance.pdr_override()

def get_data(stocks, start, end):
  data = pdr.get_data_yahoo(stocks, start, end)
  data = data[CLOSE_KEY]
  returns = data.pct_change()
  means = returns.mean()
  covariance_matrix = returns.cov()
  return means, covariance_matrix

stocks = ["AAPL", "GOOG", "TSLA"]
weights = [0.3, 0.4, 0.3]
stocks = [stock for stock in stocks]
end_date = datetime.now()
start_date = end_date - timedelta(days=SAMPLE_NUMBER_OF_DAYS)

means, covariance_matrix = get_data(stocks, start_date, end_date)

weighted_means = np.full(shape=(NUMBER_OF_DAYS, len(weights)), fill_value=means)
weighted_means = weighted_means.T

portfolio_sims = np.full(shape=(NUMBER_OF_DAYS, NUMBER_OF_SIMS), fill_value=0.0)

for m in range(0, NUMBER_OF_SIMS):
  # MC loop
  # Cholesky decomposition (check doc later)
  Z = np.random.normal(size=(NUMBER_OF_DAYS, len(weights)))
  L = np.linalg.cholesky(covariance_matrix)
  daily_returns = weighted_means + np.inner(L, Z)
  portfolio_sims[:, m] = np.cumprod(np.inner(weights, daily_returns.T) + 1) * INITIAL_PORTFOLIO_VALUE

plt.plot(portfolio_sims)
plt.ylabel('Portfolio Value $')
plt.xlabel('Days')
plt.title('Monte Carlo simulations for your portfolio')
plt.show()