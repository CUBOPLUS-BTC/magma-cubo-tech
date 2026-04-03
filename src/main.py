from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.config import settings
from app.auth import auth_router
from app.scoring import ScoringEngine
from app.scoring.schemas import ScoreResponse
from app.services import PriceAggregator
from app.simulator.routes import router as simulator_router
from app.remittance.routes import router as remittance_router


engine = ScoringEngine()
price_aggregator = PriceAggregator(settings.COINGECKO_API_KEY)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="SatsScore API",
    description="Bitcoin Financial Intelligence",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(simulator_router)
app.include_router(remittance_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "satsscore-backend"}


@app.get("/")
async def root():
    return {"message": "SatsScore API - Don't trust, verify"}


@app.get("/price")
async def get_price():
    try:
        return await price_aggregator.get_verified_price()
    except Exception as e:
        return {
            "error": str(e),
            "price_usd": 0,
            "sources_count": 0,
            "has_warning": True,
        }


@app.get("/score/{address}", response_model=ScoreResponse)
async def get_score(address: str):
    return await engine.calculate_score(address)
