import numpy as np
import pandas as pd
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

# We will need to handle a portfolio of one stock and the cov matrix
def get_data(stocks, start, end):
  data = pdr.get_data_yahoo(stocks, start, end)
  data = data[CLOSE_KEY]
  returns = data.pct_change()
  means = returns.mean()
  covariance_matrix = returns.cov()
  return means, covariance_matrix

def get_monte_carlo_simulations(weights, means, covariance_matrix, number_of_days, number_of_sims, initial_portfolio_value):
  weighted_means = np.full(shape=(number_of_days, len(weights)), fill_value=means)
  weighted_means = weighted_means.T
  portfolio_sims = np.full(shape=(number_of_days, number_of_sims), fill_value=0.0)

  for m in range(0, number_of_sims):
    # MC loop
    # Cholesky decomposition (check doc later)
    Z = np.random.normal(size=(number_of_days, len(weights)))
    L = np.linalg.cholesky(covariance_matrix)
    daily_returns = weighted_means + np.inner(L, Z)
    portfolio_sims[:, m] = np.cumprod(np.inner(weights, daily_returns.T) + 1) * initial_portfolio_value

  return portfolio_sims

def mcVaR(returns, alpha=5):
  if (isinstance(returns, pd.Series)):
    return np.percentile(returns, alpha)

  raise TypeError('Not a panda series')

def mcCVaR(returns, alpha=5):
  if (isinstance(returns, pd.Series)):
    belowVaR = returns <= mcVaR(returns, alpha=alpha)
    return returns[belowVaR].mean()

  raise TypeError('Not a panda series')

def plot_sims(figure_number, stocks, weights, data):
  plt.figure(figure_number)
  plt.plot(data)
  plt.ylabel('Portfolio Value $')
  plt.xlabel('Days')
  plt.title(f"Monte Carlo simulations for your portfolio: {[f'{stocks[i]} {weights[i]}' for i in range(0, len(stocks))]}")

stocks_1 = ["AAPL", "GOOG", "TSLA"]
weights_1 = [0.3, 0.4, 0.3]

stocks_2 = ["XEQT.TO", "HXQ.TO"]
weights_2 = [0.99, 0.01]

end_date = datetime.now()
start_date = end_date - timedelta(days=SAMPLE_NUMBER_OF_DAYS)

means_1, covariance_matrix_1 = get_data(stocks_1, start_date, end_date)
means_2, covariance_matrix_2 = get_data(stocks_2, start_date, end_date)

portfolio_sims_1 = get_monte_carlo_simulations(weights_1, means_1, covariance_matrix_1, NUMBER_OF_DAYS, NUMBER_OF_SIMS, INITIAL_PORTFOLIO_VALUE)
portfolio_sims_2 = get_monte_carlo_simulations(weights_2, means_2, covariance_matrix_2, NUMBER_OF_DAYS, NUMBER_OF_SIMS, INITIAL_PORTFOLIO_VALUE)

# plot_sims(1, stocks_1, weights_1, portfolio_sims_1)
# plot_sims(2, stocks_2, weights_2, portfolio_sims_2)

results_1 = pd.Series(portfolio_sims_1[-1, :])
results_2 = pd.Series(portfolio_sims_2[-1, :])
print('SIM1 -> VaR ', mcVaR(results_1, alpha=5), 'CVaR ', mcCVaR(results_1, alpha=5))
print('SIM2 -> VaR ', mcVaR(results_2, alpha=5), 'CVaR ', mcCVaR(results_2, alpha=5))

# plt.show()

number_of_trials = 20
number_of_simulations = [100, 1000, 10000]

for number_of_simulation in number_of_simulations:
  all_returns = []
  for _ in range(0, number_of_trials):
    sim = get_monte_carlo_simulations(weights_1, means_1, covariance_matrix_1, NUMBER_OF_DAYS, number_of_simulation, INITIAL_PORTFOLIO_VALUE)
    returns = pd.Series(sim[-1, :])
    all_returns.append(returns)

  full_series = pd.concat(all_returns)
  mean = full_series.mean()
  std = full_series.std()

  print(f'Number of sims ({number_of_simulation}) - Expected return for ["AAPL", "GOOG", "TSLA"]: {round(mean, 3)} +/- {round(1.96 * std, 3)} with 95% confidence')
