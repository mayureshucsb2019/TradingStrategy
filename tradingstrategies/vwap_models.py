from pydantic import BaseModel, Field, model_validator
from enum import Enum

class TradeAction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class TradeConfig(BaseModel):
    username: str
    password: str
    server: str
    port: int
    ticker: str
    number_of_shares_to_fill: int = Field(default=100000, gt=0)
    number_of_trades: int = Field(default=10, gt=0)
    action: TradeAction

    @model_validator(mode="before")
    @classmethod
    def check_missing_fields(cls, values):
        missing_fields = [field for field in cls.__annotations__ if field not in values or values[field] is None]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        return values