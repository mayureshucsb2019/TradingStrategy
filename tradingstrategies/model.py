from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from enum import Enum

class AuthConfig(BaseModel):
    """
    Represents authentication details for API requests.
    """
    username: str = Field(..., title="API Username")
    password: str = Field(..., title="API Password")
    server: str = Field(..., title="Server Address")
    port: int = Field(..., title="Server Port")

class OrderRequest(BaseModel):
    """
    Represents an order request to be sent to the API.
    """
    ticker: str = Field(..., title="Stock Ticker")
    type: str = Field(..., title="Order Type", pattern="^(MARKET|LIMIT)$")
    quantity: int = Field(..., title="Quantity of Stocks", gt=0)
    action: str = Field(..., title="Order Action", pattern="^(BUY|SELL)$")
    price: Optional[float] = Field(None, title="Price for LIMIT Orders")
    dry_run: int = Field(0, title="Dry Run Mode (0=execute, 1=simulate)")

    @field_validator("price")
    def check_price(cls, value, values):
        """
        Ensures price is provided for LIMIT orders.
        """
        if values.get("type") == "LIMIT" and value is None:
            raise ValueError("Price must be specified for LIMIT orders.")
        return value
    
class OrderResponse(BaseModel):
    """
    Represents the response for a placed order.
    """
    order_id: int = Field(..., example=1221, title="Order ID")
    period: int = Field(..., example=1, title="Trading Period")
    tick: int = Field(..., example=10, title="Tick")
    trader_id: str = Field(..., example="trader49", title="Trader ID")
    ticker: str = Field(..., example="CRZY", title="Ticker Symbol (Case Sensitive)")
    type: Literal["MARKET", "LIMIT"] = Field(..., example="LIMIT", title="Order Type")
    quantity: float = Field(..., example=100, title="Order Quantity")
    action: Literal["BUY", "SELL"] = Field(..., example="BUY", title="Order Action")
    price: Optional[float] = Field(None, example=14.21, title="Order Price")  # Will be null if type is MARKET
    quantity_filled: float = Field(..., example=10, title="Quantity Filled")
    vwap: Optional[float] = Field(None, example=14.21, title="Volume-Weighted Avg Price")
    status: Literal["OPEN", "TRANSACTED", "CANCELLED"] = Field(..., example="OPEN", title="Order Status")

class OHLCParams(BaseModel):
    """
    Represents parameters for retrieving OHLC history for a security.
    """
    ticker: str = Field(..., title="Ticker Symbol of the Security")
    period: Optional[int] = Field(None, title="Period to retrieve data from", description="Defaults to current period if not specified")
    limit: Optional[int] = Field(20, title="Limit of results", description="Defaults to 20 if not specified")

    class Config:
        str_min_length = 1  # Ensures that the ticker is not empty
        str_strip_whitespace = True  # Strips extra whitespace

class TimeSalesParams(BaseModel):
    """
    Represents parameters for retrieving time & sales history for a security.
    """
    ticker: str = Field(..., title="Ticker Symbol of the Security")
    after: Optional[int] = Field(None, title="ID after which to retrieve data", description="Retrieve data with an ID value greater than this")
    period: Optional[int] = Field(None, title="Period to retrieve data from", description="Defaults to current period if not specified")
    limit: Optional[int] = Field(20, title="Limit of results", description="Defaults to 20 if not specified")

    class Config:
        str_min_length = 1  # Ensures that the ticker is not empty
        str_strip_whitespace = True  # Strips extra whitespace

class OrderStatus(Enum):
    OPEN = "OPEN"
    TRANSACTED = "TRANSACTED"
    CANCELLED = "CANCELLED"

class OrdersParams(BaseModel):
    """
    Represents parameters for retrieving the list of all orders.
    """
    status: Optional[OrderStatus] = Field(OrderStatus.OPEN, title="Order Status", description="Filter orders by status. Defaults to 'OPEN'.")

    class Config:
        str_strip_whitespace = True  # Strips extra whitespace from string fields


