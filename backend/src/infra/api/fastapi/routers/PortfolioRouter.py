from typing import Annotated
from fastapi import APIRouter, Query
from pydantic import BaseModel
from datetime import datetime, timedelta

from backend.src.services.PortfolioService import PortfolioService
from backend.src.domain.portfolios.MonteCarloSimulator import MonteCarloSimulator
from backend.src.infra.clients.YahooFinanceClient import YahooFinanceClient

router = APIRouter(
    prefix="/portfolios",
    tags=["portfolios"],
    responses={404: {"description": "Not found"}},
)

SAMPLE_NUMBER_OF_DAYS = 300
NUMBER_OF_DAYS = 100
NUMBER_OF_SIMS = 1000
INITIAL_PORTFOLIO_VALUE = 10000

sims = MonteCarloSimulator()
client = YahooFinanceClient()
service = PortfolioService(sims, client)

class MonteCarloSimulationRequest(BaseModel):
    stocks: list[str]
    weights: list[float]
    initial_value: float

@router.post("/monte-carlo-sims")
async def get_monte_carlo_sims(item: MonteCarloSimulationRequest):
  end_date = datetime.now()
  start_date = end_date - timedelta(days=SAMPLE_NUMBER_OF_DAYS)

  simulation = service.simulate(item.stocks, item.weights, start_date, end_date, NUMBER_OF_DAYS, NUMBER_OF_SIMS, item.initial_value)

  return {
    # "simulations": simulation.sims.tolist(),
    "number_of_simulations": NUMBER_OF_SIMS,
    "number_of_days": NUMBER_OF_DAYS,
    "VaR": simulation.VaR,
    "CVaR": simulation.CVaR,
  }

@router.post("/monte-carlo-sims/var-convergence")
async def get_monte_carlo_sims_var_convergence(item: MonteCarloSimulationRequest):
  end_date = datetime.now()
  start_date = end_date - timedelta(days=SAMPLE_NUMBER_OF_DAYS)

  vars = service.test_VaR_convergent(item.stocks, item.weights, start_date, end_date, NUMBER_OF_DAYS, NUMBER_OF_SIMS, item.initial_value)

  return vars