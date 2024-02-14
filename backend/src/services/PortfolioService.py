from threading import Thread

# TODO: Injection direction must be into domain or services not infra
from backend.src.infra.clients.YahooFinanceClient import YahooFinanceClient
from backend.src.domain.portfolios.MonteCarloSimulator import MonteCarloSimulator
from backend.src.domain.portfolios.Portfolio import Portfolio
from backend.src.domain.portfolios.Simulation import Simulation

NUMBER_OF_THREADS = 10

class PortfolioService:
  def __init__(self, monte_carlo_sims: MonteCarloSimulator, yahoo_client: YahooFinanceClient):
    self.monte_carlo_sims = monte_carlo_sims
    self.yahoo_client = yahoo_client

  def _create_portfolio(self, stocks, weights, start, end, initial_portfolio_value) -> Portfolio:
    daily_returns = self.yahoo_client.get_daily_returns_as_percentage(stocks, start, end)
    return Portfolio(
      stocks=stocks,
      weights=weights,
      initial_value=initial_portfolio_value,
      daily_returns=daily_returns
    )

  def test_VaR_convergent(self, stocks, weights, start, end, number_of_days, number_of_sims, initial_portfolio_value):
    portfolio = self._create_portfolio(stocks, weights, start, end, initial_portfolio_value)
    results = []
    threads = [Thread(target=self._simulate_parallelism_wrapper, args=(portfolio, number_of_days, number_of_sims, results)) for _ in range(0, NUMBER_OF_THREADS)]
    for thread in threads:
      thread.start()

    for thread in threads:
      thread.join()

    return [result.VaR for result in results]

  def _simulate_parallelism_wrapper(self, portfolio, number_of_days, number_of_sims, results):
    results.append(self.monte_carlo_sims.simulate(portfolio, number_of_days, number_of_sims))

  def simulate(self, stocks, weights, start, end, number_of_days, number_of_sims, initial_portfolio_value) -> Simulation:
    portfolio = self._create_portfolio(stocks, weights, start, end, initial_portfolio_value)
    return self.monte_carlo_sims.simulate(portfolio, number_of_days, number_of_sims)

