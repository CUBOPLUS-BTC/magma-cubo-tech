from fastapi import APIRouter, HTTPException
from .schemas import RemittanceRequest, RemittanceResponse
from .optimizer import RemittanceOptimizer
from .fees import FeeTracker

router = APIRouter(prefix="/remittance", tags=["remittance"])

optimizer = RemittanceOptimizer()
fee_tracker = FeeTracker()


@router.post("/compare", response_model=RemittanceResponse)
async def compare_channels(req: RemittanceRequest):
    try:
        return await optimizer.compare(
            amount_usd=req.amount_usd,
            frequency=req.frequency,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fees")
async def get_fees():
    try:
        current_fees = await fee_tracker.get_current_fees()
        best_time = await fee_tracker.get_best_send_time()
        return {
            "fees": current_fees,
            "best_time": best_time,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
