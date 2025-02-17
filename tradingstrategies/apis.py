import httpx, asyncio, random
from utility import make_encoded_header
from typing import Optional
from tradingstrategies.models import (
    AuthConfig,
    CaseDataResponse,
    OrderRequest,
    OHLCParams,
    TimeSalesParams,
    OrderStatus,
)


async def get_current_tick(auth: AuthConfig):
    """Asynchronously gets the current tick from the case status."""
    case_data = CaseDataResponse.model_validate(await query_case_status(auth))
    return case_data.tick


async def trading_status(auth: AuthConfig):
    """Asynchronously gets the trading status."""
    case_data = CaseDataResponse.model_validate(await query_case_status(auth))
    return case_data.status


async def query_case_status(auth: AuthConfig):
    """Asynchronously queries the case status API."""
    api_endpoint = f"http://{auth['server']}:{auth['port']}/v1/case"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        async with httpx.AsyncClient() as client:
            response = await client.get(api_endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error querying case status: {e}")
        return None


async def query_trader_info(auth: AuthConfig):
    """Asynchronously queries the trader information API."""
    api_endpoint = f"http://{auth['server']}:{auth['port']}/v1/trader"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        async with httpx.AsyncClient() as client:
            response = await client.get(api_endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error querying trader info: {e}")
        return None


async def query_trading_limits(auth: AuthConfig):
    """Asynchronously queries trading limits."""
    api_endpoint = f"http://{auth['server']}:{auth['port']}/v1/limits"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        async with httpx.AsyncClient() as client:
            response = await client.get(api_endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error querying trading limits: {e}")
        return None


async def query_recent_news(auth: AuthConfig):
    """Asynchronously queries recent news."""
    api_endpoint = f"http://{auth['server']}:{auth['port']}/v1/news"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        async with httpx.AsyncClient() as client:
            response = await client.get(api_endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error querying recent news: {e}")
        return None


# NOT WORKING
async def query_assets(auth: AuthConfig, ticker: str):
    """
    Queries the assets API for a specific ticker.

    Args:
        auth: AuthConfig model containing authentication details.
        ticker: The asset ticker symbol.

    Returns:
        JSON response from the API if successful, otherwise None.
    """
    api_endpoint = f"http://{auth['server']}:{auth['port']}/v1/assets"
    # Construct query parameters
    params = {"ticker": ticker}
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        async with httpx.AsyncClient() as client:
            response = await client.get(api_endpoint, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error querying assets: {e}")
        return None


# NOT WORKING
async def query_asset_history(auth: AuthConfig):
    """Asynchronously queries asset history."""
    api_endpoint = f"http://{auth['server']}:{auth['port']}/v1/assets/history"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        async with httpx.AsyncClient() as client:
            response = await client.get(api_endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error querying asset history: {e}")
        return None


async def query_securities(auth: AuthConfig, ticker: Optional[str] = None):
    """Asynchronously queries available securities."""
    api_endpoint = f"http://{auth['server']}:{auth['port']}/v1/securities"
    params = {"ticker": ticker} if ticker else {}

    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        async with httpx.AsyncClient() as client:
            response = await client.get(api_endpoint, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error querying securities: {e}")
        return None


async def query_security_order_book(auth: AuthConfig, ticker: str, limit: int = 20):
    """Asynchronously queries the order book for securities."""
    api_endpoint = f"http://{auth['server']}:{auth['port']}/v1/securities/book"
    params = {"ticker": ticker, "limit": limit}

    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        async with httpx.AsyncClient() as client:
            response = await client.get(api_endpoint, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error querying order book: {e}")
        return None


async def query_security_ohlc_history(auth: AuthConfig, ohlc_params: OHLCParams):
    """Asynchronously queries security history (OHLC)."""
    api_endpoint = f"http://{auth['server']}:{auth['port']}/v1/securities/history"
    params = ohlc_params.model_dump(exclude_unset=True)

    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        async with httpx.AsyncClient() as client:
            response = await client.get(api_endpoint, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error querying security history: {e}")
        return None


async def query_time_and_sales(auth: AuthConfig, time_sales_params: TimeSalesParams):
    """Asynchronously queries time and sales history for a security."""
    api_endpoint = f"http://{auth['server']}:{auth['port']}/v1/securities/tas"
    params = time_sales_params.model_dump(exclude_unset=True)

    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        async with httpx.AsyncClient() as client:
            response = await client.get(api_endpoint, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error querying time and sales: {e}")
        return None


async def query_orders(auth: AuthConfig, status: Optional[OrderStatus] = None):
    """
    Asynchronously fetches a list of orders with the specified status.

    Args:
        auth: AuthConfig model containing authentication details.
        status: The status of the orders to filter by. Defaults to "OPEN".

    Returns:
        The JSON response from the API containing orders if successful, otherwise None.
    """
    api_endpoint = f"http://{auth['server']}:{auth['port']}/v1/orders"
    params = {"status": status.value} if status else {}

    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        async with httpx.AsyncClient() as client:
            response = await client.get(api_endpoint, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error during API request: {e}")
        return None


async def post_order(auth: AuthConfig, order_details: OrderRequest):
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
    url = f"http://{auth['server']}:{auth['port']}/v1/orders"

    # Construct query parameters
    params = {
        "ticker": order_details.ticker,
        "type": order_details.type,
        "quantity": order_details.quantity,
        "action": order_details.action,
        "dry_run": order_details.dry_run,
    }

    if order_details.type == "LIMIT":
        if order_details.price is None:
            raise ValueError("Price must be specified for LIMIT orders.")
        params["price"] = order_details.price

    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error placing order: {e}")
        return None


async def chunk_order(
    auth: AuthConfig, order_details: OrderRequest, batch_size: int = 10000
):
    quantity = order_details.quantity
    while True:
        if quantity >= batch_size:
            order_details.quantity = batch_size
            quantity -= batch_size
        elif quantity > 0 and quantity < batch_size:
            order_details.quantity = quantity
            quantity = 0
        else:
            break
        await post_order(auth, order_details)
        await asyncio.sleep(0.1)


async def market_square_off_all_tickers(auth, batch_size: int = 10000):
    securities_data = await query_securities(auth)  # Fetch all tickers automatically
    for security in securities_data:
        asyncio.create_task(
            market_square_off_ticker(auth, security["ticker"], batch_size)
        )


async def market_square_off_ticker(
    auth: AuthConfig, ticker: str, batch_size: int = 10000
):
    securities_data = await query_securities(auth, ticker)
    while int(securities_data[0]["position"]) != 0:
        if securities_data[0]["position"] > 0:
            action = "SELL"
        else:
            action = "BUY"

        if abs(securities_data[0]["position"]) > batch_size:
            quantity = batch_size
        else:
            quantity = abs(securities_data[0]["position"])

        order_details = OrderRequest(
            ticker=ticker, type="MARKET", quantity=quantity, action=action, dry_run=0
        )
        await post_order(auth, order_details)
        await asyncio.sleep(0.1)
        securities_data = await query_securities(auth, ticker)
    print(f"Trade for {ticker} squared off")


async def limit_square_off_ticker(
    auth: AuthConfig,
    ticker: str,
    action: str,
    price: int,
    quantity: int,
    batch_size: int = 10000,
):
    order_details = OrderRequest(
        ticker=ticker,
        type="LIMIT",
        quantity=quantity,
        action=action,
        price=price,
        dry_run=0,
    )
    await chunk_order(auth, order_details, batch_size)
    print(f"Trade for {action} {quantity} {ticker} placed at limit of {price}")


async def limit_square_off_ticker_randomized_price(
    auth: AuthConfig,
    ticker: str,
    action: str,
    price: int,
    quantity: int,
    batch_size: int = 10000,
):
    while True:
        random_choice = random.choice([0, 1, 2])
        # TODO: if error happens then this computation cannot be recovered back, add new logic @mayuresh
        if quantity >= batch_size:
            order_details = OrderRequest(
                ticker=ticker,
                type="MARKET" if random_choice == 0 else "LIMIT",
                quantity=batch_size,
                price=(
                    None
                    if random_choice == 0
                    else (
                        price - 0.1 * random_choice
                        if action == "BUY"
                        else price + 0.1 * random_choice
                    )
                ),
                action=action,
                dry_run=0,
            )
            quantity -= batch_size
        elif quantity > 0 and quantity < batch_size:
            order_details = OrderRequest(
                ticker=ticker,
                type="MARKET" if random_choice == 0 else "LIMIT",
                quantity=quantity,
                price=None if random_choice == 0 else price - 0.1 * random_choice,
                action=action,
                dry_run=0,
            )
            quantity = 0
        else:
            break
        try:
            await post_order(auth, order_details)
            print(
                f"Trade for {action} {order_details.quantity} {ticker} placed at  {order_details.price}"
            )
        except Exception as e:
            print(f"An error occurred while posting the order {order_details}: {e}")
        await asyncio.sleep(0.1)


async def stop_loss_square_off_ticker(
    auth: AuthConfig,
    tender_id: int,
    ticker: str,
    profit_price: float,
    quantity: int,
    action: str,
    stoploss_price: float,
    batch_size: int = 5000,
    square_off_time: int = 297,
):
    print(
        f"Started process for Tender-{tender_id} ticker:{ticker} action:{action } profit_price:{profit_price}"
    )
    await asyncio.sleep(1)
    while quantity > 0:
        if await get_current_tick(auth) >= square_off_time:
            print(f"square off time hit, getting out of while loop")
            break
        # Get the last price of ticker to make a stop loss decision
        securities_data = await query_securities(auth, ticker)
        last_price = securities_data[0]["last"]
        # print(f"Last price for Tender-{tender_id} ticker:{ticker} action:{action } squareoff:{squareoff_price} last:{last_price}")
        if action == "SELL":
            # Stop loss so SELL all remaining quantity that you did BUY earlier
            if last_price <= stoploss_price:  # For SELL Stop-Loss
                print(
                    f"Stop loss triggered for ticker:{ticker} action:{action } quantity:{quantity} stoploss_price:{stoploss_price} last:{last_price}"
                )
                order_details = OrderRequest(
                    ticker=ticker,
                    type="MARKET",
                    quantity=quantity,
                    action=action,
                    dry_run=0,
                )
                await chunk_order(auth=auth, order_details=order_details)
                quantity = 0
            # As last_price is larger than squareoff price, sell in batches and keep track of remaining quantity
            elif last_price >= profit_price:
                sell_quantity = min(quantity, batch_size)
                order_details = OrderRequest(
                    ticker=ticker,
                    type="MARKET",
                    quantity=sell_quantity,
                    action=action,
                    dry_run=0,
                )
                quantity = max(0, quantity - sell_quantity)
                # print(f"order detail {order_details}")
                await post_order(auth, order_details)
                print(
                    f"Batch {action} {sell_quantity} Tender-{tender_id} ticker{ticker} last_price:{last_price}  profit_price:{profit_price}"
                )
        else:
            # Stop loss so BUY all remaining quantity that you did SELL earlier
            if last_price >= stoploss_price:
                print(
                    f"Stop loss triggered for ticker:{ticker} action:{action } quantity:{quantity} stoploss_price:{stoploss_price} last:{last_price}"
                )
                order_details = OrderRequest(
                    ticker=ticker,
                    type="MARKET",
                    quantity=quantity,
                    action=action,
                    dry_run=0,
                )
                await chunk_order(auth=auth, order_details=order_details)
                quantity = 0
            # As last_price is lesser than squareoff price, BUY in batches and keep track of remaining quantity
            elif last_price <= profit_price:
                buy_quantity = min(quantity, batch_size)
                order_details = OrderRequest(
                    ticker=ticker,
                    type="MARKET",
                    quantity=buy_quantity,
                    action=action,
                    dry_run=0,
                )
                quantity = max(0, quantity - buy_quantity)
                # print(f"order detail {order_details}")
                await post_order(auth, order_details)
                print(
                    f"Batch {action} {buy_quantity} Tender-{tender_id} ticker {ticker} last_price:{last_price}  profit_price:{profit_price}"
                )
        # print(f"Working on  ticker:{ticker} action:{action } quantity:{quantity} stoploss_price:{stoploss_price} last:{last_price} profit_price:{profit_price}")
        await asyncio.sleep(0.5)
    print(f"Tender-{tender_id} {ticker} was squared off")


async def query_order_details(auth: AuthConfig, order_id: int):
    """Asynchronously queries specific order details."""
    api_endpoint = f"http://{auth['server']}:{auth['port']}/v1/orders/{order_id}"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        async with httpx.AsyncClient() as client:
            response = await client.get(api_endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error querying order details for {order_id}: {e}")
        return None


async def cancel_order(auth: AuthConfig, order_id: int):
    """Asynchronously cancels an open order by ID."""
    api_endpoint = f"http://{auth['server']}:{auth['port']}/v1/orders/{order_id}"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        async with httpx.AsyncClient() as client:
            response = await client.delete(api_endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error cancelling order {order_id}: {e}")
        return None


async def cancel_all_open_order(auth: AuthConfig):
    orders = await query_orders(auth, OrderStatus.OPEN)
    print(f"Open orders are {orders}")
    while orders:
        for i, order in enumerate(orders):
            try:
                # Attempt to cancel the order
                await cancel_order(auth, order["order_id"])
                print(f"Cancelled {i} {order['order_id']} of {len(orders)} orders")
            except Exception as e:
                # Catch any other errors that occur
                print(
                    f"An error occurred while cancelling the order {i} {order['order_id']} of {len(orders)} orders: {e}"
                )
            await asyncio.sleep(0.1)
        orders = await query_orders(auth, OrderStatus.OPEN)
    print("Cancelled all open orders")


async def post_tender(auth: AuthConfig, tender_id: int, price: float):
    """Asynchronously accepts a tender offer with the given price."""
    api_endpoint = f"http://{auth['server']}:{auth['port']}/v1/tenders/{tender_id}"
    params = {"price": price}
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        async with httpx.AsyncClient() as client:
            response = await client.post(api_endpoint, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error posting tender {tender_id}: {e}")
        return None


async def decline_tender(auth: AuthConfig, tender_id: int):
    """Asynchronously declines a tender offer."""
    api_endpoint = f"http://{auth['server']}:{auth['port']}/v1/tenders/{tender_id}"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        async with httpx.AsyncClient() as client:
            response = await client.delete(api_endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error declining tender {tender_id}: {e}")
        return None


async def is_tender_processed(auth: AuthConfig, ticker: str):
    """Asynchronously checks if a tender has been processed."""
    securities_data = await query_securities(auth, ticker)
    return securities_data[0]["position"] != 0.0 if securities_data else False


async def query_tenders(auth: AuthConfig):
    """Asynchronously queries all active tenders."""
    api_endpoint = f"http://{auth['server']}:{auth['port']}/v1/tenders"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        async with httpx.AsyncClient() as client:
            response = await client.get(api_endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error querying tenders: {e}")
        return None


async def query_leases(auth: AuthConfig):
    """Asynchronously queries all leased assets."""
    api_endpoint = f"http://{auth['server']}:{auth['port']}/v1/leases"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        async with httpx.AsyncClient() as client:
            response = await client.get(api_endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error querying leases: {e}")
        return None


async def query_lease_details(auth: AuthConfig, lease_id: int):
    """Asynchronously queries details of a specific lease."""
    api_endpoint = f"http://{auth['server']}:{auth['port']}/v1/leases/{lease_id}"
    try:
        headers = make_encoded_header(auth["username"], auth["password"])
        async with httpx.AsyncClient() as client:
            response = await client.get(api_endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error querying lease details for {lease_id}: {e}")
        return None
