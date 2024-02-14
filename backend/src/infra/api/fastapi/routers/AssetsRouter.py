from fastapi import APIRouter, Query

from backend.src.infra.clients.YahooFinanceClient import YahooFinanceClient

router = APIRouter(
    prefix="/assets",
    tags=["assets"],
    responses={404: {"description": "Not found"}},
)

client = YahooFinanceClient()

# This does not search yet, yahoo does not provide a search api
@router.get("/tickers/search")
async def get_monte_carlo_sims(query: str = Query(..., min_length=3)):
  results = client.search_tickers(query)

  print(results)

  return {
    "results": results,
    "count": len(results),
  }