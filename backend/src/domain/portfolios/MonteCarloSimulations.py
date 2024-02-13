import numpy as np

class MonteCarloSimulations:
  def __init__(self):
    pass

  def create_monte_carlo_simulations(self, weights, means, covariance_matrix, number_of_days, number_of_sims, initial_portfolio_value):
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
