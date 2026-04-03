from fastapi import APIRouter, HTTPException
from .schemas import SimulationRequest, SimulationResponse
from .volatility import VolatilitySimulator
from .conversion import ConversionStrategy

router = APIRouter(prefix="/simulate", tags=["simulator"])

simulator = VolatilitySimulator()
conversion = ConversionStrategy()


@router.post("/volatility", response_model=SimulationResponse)
async def simulate_volatility(req: SimulationRequest):
    try:
        return await simulator.simulate(
            amount_usd=req.amount_usd,
            days_history=req.days_history,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conversion")
async def simulate_conversion(req: SimulationRequest):
    try:
        return await conversion.recommend(
            amount_usd=req.amount_usd,
            days_history=req.days_history,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
