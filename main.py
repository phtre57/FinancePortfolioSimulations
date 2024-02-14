from fastapi import FastAPI
from backend.src.infra.api.fastapi.routers import PortfolioRouter
from backend.src.infra.api.fastapi.routers import AssetsRouter
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(PortfolioRouter.router)
app.include_router(AssetsRouter.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}