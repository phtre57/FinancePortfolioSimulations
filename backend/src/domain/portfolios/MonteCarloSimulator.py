import numpy as np
import pandas as pd

from backend.src.domain.portfolios.Simulation import Simulation
from backend.src.domain.portfolios.Portfolio import Portfolio

class MonteCarloSimulator:
  def __init__(self):
    self.BASE_ALPHA = 5

  def simulate(self, portfolio: Portfolio, number_of_days: int, number_of_sims: int) -> Simulation:
    means = portfolio.get_daily_returns_means()
    covariance_matrix = portfolio.get_daily_returns_cov_matrix()
    weights = portfolio.weights
    initial_portfolio_value = portfolio.initial_value
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

    sims = portfolio_sims.T
    return Simulation(sims, self._VaR(sims, alpha=self.BASE_ALPHA), self._CVaR(sims, alpha=self.BASE_ALPHA))

  def _VaR(self, sims, alpha=5):
    end_returns = pd.Series(sims[-1])
    return np.percentile(end_returns, alpha)

  def _CVaR(self, sims, alpha=5):
    end_returns = pd.Series(sims[-1])
    belowVaR = end_returns <= self._VaR(sims, alpha=alpha)
    return end_returns[belowVaR].mean()
