import requests,time
from utility import make_encoded_header
from typing import Optional
from tradingstrategies.models import AuthConfig, CaseDataResponse, OrderRequest, OHLCParams, TimeSalesParams, OrderStatus
import asyncio

ticker_locks = {}

def get_current_tick(auth: AuthConfig):
    case_data = CaseDataResponse.model_validate(query_case_status(auth))
    return case_data.tick

def trading_status(self):
    case_data = CaseDataResponse.model_validate(query_case_status(self.auth))
    return case_data.status

def query_case_status(auth: AuthConfig):
    """Queries the case status API."""
    api_endpoint = f"http://{auth["server"]}:{auth["port"]}/v1/case"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        response = requests.get(api_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying case status: {e}")
        return None

def query_trader_info(auth: AuthConfig):
    """Queries the trader information API."""
    api_endpoint = f"http://{auth["server"]}:{auth["port"]}/v1/trader"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        response = requests.get(api_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying trader info: {e}")
        return None

def query_trading_limits(auth: AuthConfig):
    """Queries trading limits."""
    api_endpoint = f"http://{auth["server"]}:{auth["port"]}/v1/limits"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        response = requests.get(api_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying trading limits: {e}")
        return None

def query_recent_news(auth: AuthConfig):
    """Queries recent news."""
    api_endpoint = f"http://{auth["server"]}:{auth["port"]}/v1/news"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        response = requests.get(api_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying recent news: {e}")
        return None

# NOT WORKING
def query_assets(auth: AuthConfig, ticker: str):
    """
    Queries the assets API for a specific ticker.

    Args:
        auth: AuthConfig model containing authentication details.
        ticker: The asset ticker symbol.

    Returns:
        JSON response from the API if successful, otherwise None.
    """
    api_endpoint = f"http://{auth["server"]}:{auth["port"]}/v1/assets"
    # Construct query parameters
    params = {
        "ticker": ticker
    }
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        response = requests.get(api_endpoint, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying assets: {e}")
        return None

# NOT WORKING
def query_asset_history(auth: AuthConfig):
    """Queries asset history."""
    api_endpoint = f"http://{auth["server"]}:{auth["port"]}/v1/assets/history"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        response = requests.get(api_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying asset history: {e}")
        return None

def query_securities(auth: AuthConfig, ticker: str =None):
    """Queries available securities."""
    api_endpoint = f"http://{auth["server"]}:{auth["port"]}/v1/securities"
    if ticker:
        params = {
            "ticker": ticker
        }
    else:
        params = {}
    
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        response = requests.get(api_endpoint, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying securities: {e}")
        return None

def query_security_order_book(auth: AuthConfig, ticker: str, limit: int = 20):
    """Queries order book for securities."""
    api_endpoint = f"http://{auth["server"]}:{auth["port"]}/v1/securities/book"
    params = {
            "ticker": ticker,
            "limit":limit
        }
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        response = requests.get(api_endpoint, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying order book: {e}")
        return None

def query_security_ohlc_history(auth: AuthConfig, ohlc_params: OHLCParams):
    """Queries security history."""
    api_endpoint = f"http://{auth["server"]}:{auth["port"]}/v1/securities/history"
    params = ohlc_params.model_dump(exclude_unset=True)
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        response = requests.get(api_endpoint, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying security history: {e}")
        return None

def query_time_and_sales(auth: AuthConfig, time_sales_params: TimeSalesParams):
    """Queries time and sales history for a security."""
    api_endpoint = f"http://{auth["server"]}:{auth["port"]}/v1/securities/tas"
    params = time_sales_params.model_dump(exclude_unset=True)
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        response = requests.get(api_endpoint, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying time and sales: {e}")
        return None

def query_orders(auth: AuthConfig, status: Optional[OrderStatus] = None):
    """
    Fetches a list of orders with the specified status.
    
    Args:
        auth: AuthConfig model containing authentication details.
        status: The status of the orders to filter by. Defaults to "OPEN".
        
    Returns:
        The JSON response from the API containing orders if successful, otherwise None.
    """
    api_endpoint = f"http://{auth["server"]}:{auth["port"]}/v1/orders"
    
    params = {}

    # Only add the 'status' parameter if it's not None
    if status:
        params["status"] = status.value

    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        response = requests.get(api_endpoint, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None

def post_order(auth: AuthConfig, order_details: OrderRequest):
    """
    Places a new order using the API.

    Args:
        auth["username"]: API auth["username"].
        auth["password"]: API auth["password"].
        auth["server"]: API auth["server"] address.
        auth["port"]: API auth["port"].
        ticker: Stock ticker symbol.
        order_type: Order type ("MARKET" or "LIMIT").
        quantity: Number of shares.
        action: Order action ("BUY" or "SELL").
        price: Price per share (Required for LIMIT orders).
        dry_run: Simulate execution (0 for real execution, 1 for simulation).

    Returns:
        JSON response from the API if successful, otherwise None.
    """
    url = f"http://{auth["server"]}:{auth["port"]}/v1/orders"

    # Construct query parameters
    params = {
        "ticker": order_details.ticker,
        "type": order_details.type,
        "quantity": order_details.quantity,
        "action": order_details.action,
        "dry_run": order_details.dry_run
    }

    if order_details.type == "LIMIT":
        if order_details.price is None:
            raise ValueError("Price must be specified for LIMIT orders.")
        params["price"] = order_details.price

    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        response = requests.post(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error placing order: {e}")
        return None

def chunk_order(auth: AuthConfig, order_details: OrderRequest):
    quantity = order_details.quantity
    while True:
        if quantity >= 10000:
            order_details.quantity = 10000
            quantity -= 10000
        elif quantity > 0 and quantity < 10000:
            order_details.quantity = quantity
            quantity = 0
        else:
            break
        post_order(auth, order_details)

def instant_square_off_ticker(auth: AuthConfig, ticker: str, batch_size: int = 10000):
    securities_data = query_securities(auth, ticker)
    while int(securities_data[0]["position"]) != 0:
        if securities_data[0]["position"] > 0 :
            action = "SELL"
        else:
            action = "BUY"

        if abs(securities_data[0]["position"]) > batch_size:
            quantity = batch_size
        else:
            quantity = abs(securities_data[0]["position"])
        
        order_details = OrderRequest(
                        ticker=ticker,
                        type="MARKET",
                        quantity=quantity,
                        action=action,
                        dry_run=0
                    )        
        post_order(auth, order_details)
        securities_data = query_securities(auth, ticker)
    print(f"Trade for {ticker} squared off")

async def stop_loss_square_off_ticker(auth: AuthConfig, tender_id: int, ticker: str, squareoff_price: float, quantity: int, action: str, loss_percent: float = 0.1, batch_size: int = 5000):
    print(f"Started process for Tender-{tender_id} ticker:{ticker} action:{action } squareoff:{squareoff_price}")
    await asyncio.sleep(1)
    if ticker not in ticker_locks:
        ticker_locks[ticker] = asyncio.Lock()  # Create a lock only if it doesn't exist
        print(f"Lock created for Tender-{tender_id} ticker {ticker}")
    else:
        print(f"Lock exists for Tender-{tender_id} ticker {ticker}")
    while quantity > 0:
        if get_current_tick(auth) >= 297: 
            # acquire lock so that two process of same ticker shouldn't square off at the same time
            async with ticker_locks[ticker]:
                instant_square_off_ticker(auth, ticker, batch_size)
                print(f"Instant square off of Tender-{tender_id} ticker {ticker} as time limit reached")
            break
        # Get the last price of ticker to make a stop loss decision
        last_price = query_securities(auth,ticker)[0]["last"]   
        # print(f"Last price for Tender-{tender_id} ticker:{ticker} action:{action } squareoff:{squareoff_price} last:{last_price}")   
        if action == "SELL":
            # Stop loss so SELL all remaining quantity that you did BUY earlier
            if last_price <= squareoff_price * (1 - loss_percent):  # For SELL Stop-Loss
                print(f"Stop loss triggered for ticker:{ticker} action:{action } squareoff:{squareoff_price} last:{last_price}")
                order_details = OrderRequest(
                                ticker=ticker,
                                type="MARKET",
                                quantity=quantity,
                                action=action,
                                dry_run=0
                            )
                chunk_order(auth=auth, order_details=order_details)
                quantity = 0 
                print(f"Stop loss for {action} Tender-{tender_id} ticker {ticker}")
            # As last_price is larger than squareoff price, sell in batches and keep track of remaining quantity
            elif last_price >= squareoff_price:
                sell_quantity = min(quantity, batch_size)
                order_details = OrderRequest(
                            ticker=ticker,
                            type="MARKET",
                            quantity=sell_quantity,
                            action=action,
                            dry_run=0
                        )
                quantity = max(0, quantity - sell_quantity)
                print(f"order detail {order_details}")
                post_order(auth, order_details)
                print(f"Batch {action} Tender-{tender_id} ticker {ticker}")
        else:
            # Stop loss so BUY all remaining quantity that you did SELL earlier
            if last_price >= squareoff_price * (1 + loss_percent):
                print(f"Stop loss triggered for ticker:{ticker} action:{action } squareoff:{squareoff_price} last:{last_price}")
                order_details = OrderRequest(
                                ticker=ticker,
                                type="MARKET",
                                quantity=quantity,
                                action=action,
                                dry_run=0
                            )
                chunk_order(auth=auth, order_details=order_details)
                quantity = 0 
                print(f"Stop loss for {action} Tender-{tender_id} ticker {ticker}")
            # As last_price is lesser than squareoff price, BUY in batches and keep track of remaining quantity
            elif last_price <= squareoff_price:
                buy_quantity = min(quantity, batch_size)
                order_details = OrderRequest(
                            ticker=ticker,
                            type="MARKET",
                            quantity=buy_quantity,
                            action=action,
                            dry_run=0
                        )
                quantity = max(0, quantity - buy_quantity)
                print(f"order detail {order_details}")
                post_order(auth, order_details)
                print(f"Batch {action} Tender-{tender_id} ticker {ticker}")
        await asyncio.sleep(0.5)
    print(f"Tender-{tender_id} ${ticker} was squared off")

def query_order_details(auth: AuthConfig, order_id:int):
    """Queries specific order details."""
    api_endpoint = f"http://{auth["server"]}:{auth["port"]}/v1/orders/{order_id}"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        response = requests.get(api_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying order details for {order_id}: {e}")
        return None

def cancel_order(auth: AuthConfig, order_id: int):
    """
    Cancels an open order by ID.

    Args:
        username: The username for authentication.
        password: The password for authentication.
        server: The server address.
        port: The server port.
        order_id: The ID of the order to cancel.

    Returns:
        The JSON response from the API if successful, otherwise None.
    """
    api_endpoint = f"http://{auth["server"]}:{auth["port"]}/v1/orders/{order_id}"
    
    try:
        headers = make_encoded_header(auth["username"], auth["password"])  
        response = requests.delete(api_endpoint, headers=headers)
        response.raise_for_status()  
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None

def post_tender(auth: AuthConfig, tender_id: int, price: float):
    """
    Accept a tender offer with the given price.
    
    Args:
        auth: AuthConfig model containing authentication details.
        tender_id: The ID of the tender.
        price: The bid price for the tender.
        
    Returns:
        The JSON response from the API if successful, otherwise None.
    """
    api_endpoint = f"http://{auth["server"]}:{auth["port"]}/v1/tenders/{tender_id}"
    params = {"price": price}
    
    try:
        headers = make_encoded_header(auth["username"], auth["password"])  
        response = requests.post(api_endpoint, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None

def decline_tender(auth: AuthConfig, tender_id: int):
    """
    Decline a tender offer with the given tender ID.
    
    Args:
        auth: AuthConfig model containing authentication details.
        tender_id: The ID of the tender to decline.
        
    Returns:
        The JSON response from the API if successful, otherwise None.
    """
    api_endpoint = f"http://{auth["server"]}:{auth["port"]}/v1/tenders/{tender_id}"
    
    try:
        headers = make_encoded_header(auth["username"], auth["password"])  
        response = requests.delete(api_endpoint, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None

def is_tender_processed(auth: AuthConfig, ticker: str):
    securities_data = query_securities(auth, ticker)
    return securities_data[0]["position"] != 0.0

def query_tenders(auth: AuthConfig):
    """Queries all active tenders."""
    api_endpoint = f"http://{auth["server"]}:{auth["port"]}/v1/tenders"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        response = requests.get(api_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying tenders: {e}")
        return None

def query_leases(auth: AuthConfig):
    """Queries all leased assets."""
    api_endpoint = f"http://{auth["server"]}:{auth["port"]}/v1/leases"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        response = requests.get(api_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying leases: {e}")
        return None

def query_lease_details(auth: AuthConfig, lease_id):
    """Queries details of a specific lease."""
    api_endpoint = f"http://{auth["server"]}:{auth["port"]}/v1/leases/{lease_id}"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        response = requests.get(api_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying lease details for {lease_id}: {e}")
        return None
