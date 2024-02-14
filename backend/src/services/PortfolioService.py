# TODO: Injection direction must be into domain or services not infra
from backend.src.infra.clients.YahooFinanceClient import YahooFinanceClient
from backend.src.domain.portfolios.MonteCarloSimulator import MonteCarloSimulator
from backend.src.domain.portfolios.Portfolio import Portfolio

class PortfolioService:
  def __init__(self, monte_carlo_sims: MonteCarloSimulator, yahoo_client: YahooFinanceClient):
    self.monte_carlo_sims = monte_carlo_sims
    self.yahoo_client = yahoo_client

  def simulate(self, stocks, weights, start, end, number_of_days, number_of_sims, initial_portfolio_value):
    daily_returns = self.yahoo_client.get_daily_returns_as_percentage(stocks, start, end)
    portfolio = Portfolio(
      stocks=stocks,
      weights=weights,
      initial_value=initial_portfolio_value,
      daily_returns=daily_returns
    )
    return self.monte_carlo_sims.simulate(portfolio, number_of_days, number_of_sims)

