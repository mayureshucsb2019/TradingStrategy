import time, os, apis, asyncio
from rich.console import Console  # type: ignore
from rich.table import Table  # type: ignore
from dotenv import load_dotenv  # type: ignore

# Console setup for terminal output
console = Console()
# Load environment variables from .env file
load_dotenv()
# Read values from .env
AUTH = {
    "username": os.getenv("USERNAME"),
    "password": os.getenv("PASSWORD"),
    "server": os.getenv("SERVER"),
    "port": os.getenv("PORT"),
}
T3_MARKET_DEPTH_POINTS = int(os.getenv("T3_MARKET_DEPTH_POINTS"))
T3_MIN_PROFIT_MARGIN = float(os.getenv("T3_MIN_PROFIT_MARGIN"))
T3_TRADE_UNTIL_TICK = int(os.getenv("T3_TRADE_UNTIL_TICK"))
T3_MIN_VWAP_MARGIN = float(os.getenv("T3_MIN_VWAP_MARGIN"))
T3_STOP_LOSS_PERCENT = float(os.getenv("T3_STOP_LOSS_PERCENT"))
T3_BATCH_SIZE = int(os.getenv("T3_BATCH_SIZE"))
T3_SQUARE_OFF_BATCH_SIZE = int(os.getenv("T3_SQUARE_OFF_BATCH_SIZE"))

print(
    f"Hyper parameters are\n"
    + f"T3_MARKET_DEPTH_POINTS:{T3_MARKET_DEPTH_POINTS}\n"
    + f"T3_MIN_PROFIT_MARGIN:{T3_MIN_PROFIT_MARGIN}\n"
    + f"T3_TRADE_UNTIL_TICK:{T3_TRADE_UNTIL_TICK}\n"
    + f"T3_MIN_VWAP_MARGIN:{T3_MIN_VWAP_MARGIN}\n"
    + f"T3_STOP_LOSS_PERCENT:{T3_STOP_LOSS_PERCENT}\n"
    + f"T3_BATCH_SIZE:{T3_BATCH_SIZE}\n"
    + f"T3_SQUARE_OFF_BATCH_SIZE:{T3_SQUARE_OFF_BATCH_SIZE}"
)


# Function to calculate VWAP (Volume-Weighted Average Price)
def calculate_vwap(price_volume_list):
    total_volume = sum(v for _, v in price_volume_list)
    if total_volume == 0:
        return "#DIV/0!"  # Avoid division by zero
    return round(sum(p * v for p, v in price_volume_list) / total_volume, 2)


# Function to generate the Market Depth table
async def generate_market_depth(ticker: str):
    order_book = await apis.query_security_order_book(
        AUTH, ticker, T3_MARKET_DEPTH_POINTS
    )

    bids = sorted(order_book["bids"], key=lambda x: x["price"], reverse=True)[
        :T3_MARKET_DEPTH_POINTS
    ]  # Top number_of_data_points bid levels
    asks = sorted(order_book["asks"], key=lambda x: x["price"])[
        :T3_MARKET_DEPTH_POINTS
    ]  # Top number_of_data_points ask levels

    # Calculate cumulative volumes & VWAP
    cumulative_bid_vol = 0
    cumulative_ask_vol = 0
    bid_vwap_list = []
    ask_vwap_list = []

    table = Table(
        title=f"Market Depth View - {ticker}",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("BidVWAP", justify="right")
    table.add_column("Cum Bid Vol", justify="right")
    table.add_column("Bid Volume", justify="right")
    table.add_column("Bid Price", justify="right")
    table.add_column("Ask Price", justify="right")
    table.add_column("Ask Volume", justify="right")
    table.add_column("Cum Ask Vol", justify="right")
    table.add_column("AskVWAP", justify="right")

    for i in range(T3_MARKET_DEPTH_POINTS):
        # Extract bid data
        bid_price = bids[i]["price"] if i < len(bids) else 0
        bid_volume = bids[i]["quantity"] if i < len(bids) else 0
        cumulative_bid_vol += bid_volume
        bid_vwap_list.append((bid_price, bid_volume))

        # Extract ask data
        ask_price = asks[i]["price"] if i < len(asks) else 0
        ask_volume = asks[i]["quantity"] if i < len(asks) else 0
        cumulative_ask_vol += ask_volume
        ask_vwap_list.append((ask_price, ask_volume))

        # Calculate VWAPs
        bid_vwap = calculate_vwap(bid_vwap_list)
        ask_vwap = calculate_vwap(ask_vwap_list)

        # Add row to table
        table.add_row(
            str(bid_vwap),
            str(cumulative_bid_vol),
            str(bid_volume),
            str(bid_price),
            str(ask_price),
            str(ask_volume),
            str(cumulative_ask_vol),
            str(ask_vwap),
        )
    return table


async def generate_signal(
    ticker: str, price: float, action: str, quantity: int, margin: float = 0.0
):
    # Generate the market depth table
    market_depth_table = await generate_market_depth(ticker)
    # console.print(market_depth_table)

    # Convert generator to list
    bid_vwap_list = [float(cell) for cell in market_depth_table.columns[0].cells]
    ask_vwap_list = [float(cell) for cell in market_depth_table.columns[7].cells]

    # For SELL action, we look at bids
    if action == "SELL":
        bid_vwap_at_quantity = None
        for i, bid_cell in enumerate(market_depth_table.columns[1].cells):
            cumulative_bid_vol = int(float(bid_cell))

            if cumulative_bid_vol >= quantity:
                bid_vwap_at_quantity = bid_vwap_list[i]
                break

        if bid_vwap_at_quantity is None:
            bid_vwap_at_quantity = bid_vwap_list[0]

        if price - margin > bid_vwap_at_quantity:
            return (True, bid_vwap_at_quantity)
        return (False, bid_vwap_at_quantity)

    elif action == "BUY":
        ask_vwap_at_quantity = None
        for i, ask_cell in enumerate(market_depth_table.columns[6].cells):
            cumulative_ask_vol = int(float(ask_cell))

            if cumulative_ask_vol >= quantity:
                ask_vwap_at_quantity = ask_vwap_list[i]
                break

        if ask_vwap_at_quantity is None:
            ask_vwap_at_quantity = ask_vwap_list[0]

        if price + margin < ask_vwap_at_quantity:
            return (True, ask_vwap_at_quantity)
        return (False, ask_vwap_at_quantity)

    return (False, -1)


async def main():
    end_of_time_hit = False
    while True:
        tender_response = []
        if await apis.get_current_tick(AUTH) <= T3_TRADE_UNTIL_TICK:
            tender_response = await apis.query_tenders(AUTH)
        else:
            if not end_of_time_hit:
                print("End of period hit, squaring off all open positions")
                # First cancel all open orders
                await apis.cancel_all_open_order(AUTH)
                asyncio.create_task(
                    apis.market_square_off_all_tickers(AUTH, T3_SQUARE_OFF_BATCH_SIZE)
                )
                end_of_time_hit = True

        if tender_response:
            print(f"Details of tender received is: \n{tender_response}")
            for tender in tender_response:
                signal_response = await generate_signal(
                    tender["ticker"],
                    tender["price"],
                    tender["action"],
                    tender["quantity"],
                    T3_MIN_VWAP_MARGIN,
                )
                squareoff_action = "SELL" if tender["action"] == "BUY" else "BUY"
                print(f"Signal analysed: \n{signal_response}")
                if signal_response[0]:
                    securities_data = await apis.query_securities(AUTH)
                    security_position = {}
                    net_position = 0
                    gross_position = 0
                    for security in securities_data:
                        security_position[tender["ticker"]] = security["position"]
                        if tender["ticker"] == security["ticker"]:
                            tender_quantity = (
                                -1 * tender["quantity"]
                                if tender["action"] == "SELL"
                                else tender["quantity"]
                            )
                            security_position[tender["ticker"]] += tender_quantity
                        net_position += security_position[tender["ticker"]]
                        gross_position += abs(security_position[tender["ticker"]])
                    if net_position > 100000 or gross_position > 250000:
                        print(
                            f"Cannot accept this tender ${tender} net_position:{net_position} gross_position:{gross_position}"
                        )
                        print(f"Waiting for favorable condition to accept tender")
                        break
                    tender_response = await apis.post_tender(
                        AUTH, tender["tender_id"], tender["price"]
                    )
                    print(f"Tender accepted: {tender_response}")
                    if tender_response["success"]:
                        is_tender_processed_count = 0
                        is_tender_processed = await apis.is_tender_processed(
                            AUTH, tender["ticker"]
                        )
                        while not is_tender_processed:
                            await asyncio.sleep(0.1)
                            is_tender_processed_count += 1
                            print("waiting for tender to be processed")
                            is_tender_processed = await apis.is_tender_processed(
                                AUTH, tender["ticker"]
                            )
                            if is_tender_processed_count == 5:
                                break

                        profit_price = (
                            tender["price"] - T3_MIN_PROFIT_MARGIN
                            if squareoff_action == "BUY"
                            else tender["price"] + T3_MIN_PROFIT_MARGIN
                        )
                        stoploss_price = (
                            tender["price"] * (1 + T3_STOP_LOSS_PERCENT)
                            if squareoff_action == "BUY"
                            else tender["price"] * (1 - T3_STOP_LOSS_PERCENT)
                        )
                        if is_tender_processed:
                            # asyncio.create_task(
                            #     apis.stop_loss_square_off_ticker(AUTH, tender["tender_id"], tender["ticker"],
                            #                                     profit_price, tender["quantity"], squareoff_action,
                            #                                     stoploss_price=stoploss_price, batch_size=T3_BATCH_SIZE, square_off_time=T3_TRADE_UNTIL_TICK)
                            # )
                            # asyncio.create_task(
                            #     apis.market_square_off_ticker(
                            #         AUTH, tender["ticker"], T3_SQUARE_OFF_BATCH_SIZE
                            #     )
                            # )

                            asyncio.create_task(
                                apis.limit_square_off_ticker(
                                    AUTH,
                                    tender["ticker"],
                                    squareoff_action,
                                    (
                                        tender["price"] + T3_MIN_PROFIT_MARGIN
                                        if squareoff_action == "SELL"
                                        else tender["price"] - T3_MIN_PROFIT_MARGIN
                                    ),
                                    tender["quantity"],
                                    T3_SQUARE_OFF_BATCH_SIZE,
                                )
                            )

                else:
                    print(f"Waiting for favorable condition to accept tender")
        await asyncio.sleep(1)


# Run the event loop
asyncio.run(main())
