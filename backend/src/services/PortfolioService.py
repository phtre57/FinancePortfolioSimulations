# TODO: Injection direction must be into domain or services not infra
from backend.src.infra.clients.YahooFinanceClient import YahooFinanceClient
from backend.src.domain.portfolios.MonteCarloSimulations import MonteCarloSimulations

class PortfolioService:
  def __init__(self, monte_carlo_sims: MonteCarloSimulations, yahoo_client: YahooFinanceClient):
    self.monte_carlo_sims = monte_carlo_sims
    self.yahoo_client = yahoo_client

  def create_monte_carlo_simulations(self, stocks, weights, start, end, number_of_days, number_of_sims, initial_portfolio_value):
    means, covariance_matrix = self.yahoo_client.get_stocks_data(stocks, start, end)
    return self.monte_carlo_sims.create_monte_carlo_simulations(weights, means, covariance_matrix, number_of_days, number_of_sims, initial_portfolio_value)
