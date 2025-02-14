from pydantic import BaseModel

class CaseData(BaseModel):
    name: str
    period: int
    tick: int
    ticks_per_period: int
    total_periods: int
    status: str
    is_enforce_trading_limits: bool
