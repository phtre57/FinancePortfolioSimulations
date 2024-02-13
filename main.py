from fastapi import FastAPI
from src.infra.api.fastapi.routers import PortfolioRouter

app = FastAPI()

app.include_router(PortfolioRouter.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}