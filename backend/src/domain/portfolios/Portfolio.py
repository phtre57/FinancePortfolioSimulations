from pandas import Series

class Portfolio:
  def __init__(self, stocks: list[str], weights: list[float], initial_value: float, daily_returns: Series) -> None:
    self.stocks = stocks
    self.weights = weights
    self.initial_value = initial_value
    self.daily_returns = daily_returns

  def get_daily_returns_means(self):
    return self.daily_returns.mean()

  def get_daily_returns_cov_matrix(self):
    return self.daily_returns.cov()