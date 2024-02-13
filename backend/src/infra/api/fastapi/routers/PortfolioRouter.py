from typing import Annotated
from fastapi import APIRouter, Query
from datetime import datetime, timedelta

from backend.src.services.PortfolioService import PortfolioService
from backend.src.domain.portfolios.MonteCarloSimulations import MonteCarloSimulations
from backend.src.infra.clients.YahooFinanceClient import YahooFinanceClient

router = APIRouter(
    prefix="/portfolios",
    tags=["portfolios"],
    responses={404: {"description": "Not found"}},
)

SAMPLE_NUMBER_OF_DAYS = 300
NUMBER_OF_DAYS = 100
NUMBER_OF_SIMS = 100
INITIAL_PORTFOLIO_VALUE = 10000

sims = MonteCarloSimulations()
client = YahooFinanceClient()
service = PortfolioService(sims, client)


@router.get("/monte-carlo-sims")
async def get_monte_carlo_sims(stocks: Annotated[list[str] | None, Query()] = None, weights: Annotated[list[float] | None, Query()] = None, initial_value: float = INITIAL_PORTFOLIO_VALUE):
  end_date = datetime.now()
  start_date = end_date - timedelta(days=SAMPLE_NUMBER_OF_DAYS)

  portfolio_sims = service.create_monte_carlo_simulations(stocks, weights, start_date, end_date, NUMBER_OF_DAYS, NUMBER_OF_SIMS, initial_value)

  return {
    "simulations": portfolio_sims.tolist()
  }