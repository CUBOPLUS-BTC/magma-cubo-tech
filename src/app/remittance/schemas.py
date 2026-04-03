from pydantic import BaseModel
from typing import Optional


class RemittanceRequest(BaseModel):
    amount_usd: float
    frequency: str = "monthly"


class ChannelComparison(BaseModel):
    name: str
    fee_percent: float
    fee_usd: float
    amount_received: float
    estimated_time: str
    is_recommended: bool


class SendTimeRecommendation(BaseModel):
    best_time: str
    current_fee_sat_vb: int
    estimated_low_fee_sat_vb: int
    savings_percent: float


class RemittanceResponse(BaseModel):
    channels: list[ChannelComparison]
    annual_savings: float
    best_channel: str
    best_time: Optional[SendTimeRecommendation] = None
