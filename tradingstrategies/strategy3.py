import time, os, apis, asyncio
from rich.console import Console # type: ignore
from rich.table import Table # type: ignore
from dotenv import load_dotenv # type: ignore

# Console setup for terminal output
console = Console()
# Load environment variables from .env file
load_dotenv()

# Read values from .env
auth = {
    "username": os.getenv("USERNAME"),
    "password": os.getenv("PASSWORD"),
    "server": os.getenv("SERVER"),
    "port": os.getenv("PORT")
}

number_of_data_points = 20
# Function to calculate VWAP (Volume-Weighted Average Price)
def calculate_vwap(price_volume_list):
    total_volume = sum(v for _, v in price_volume_list)
    if total_volume == 0:
        return "#DIV/0!"  # Avoid division by zero
    return round(sum(p * v for p, v in price_volume_list) / total_volume, 2)

# Function to generate the Market Depth table
def generate_market_depth(ticker: str):
    order_book = apis.query_security_order_book(auth,ticker,number_of_data_points)

    bids = sorted(order_book["bids"], key=lambda x: x['price'], reverse=True)[:number_of_data_points]  # Top number_of_data_points bid levels
    asks = sorted(order_book["asks"], key=lambda x: x['price'])[:number_of_data_points]  # Top number_of_data_points ask levels

    # Calculate cumulative volumes & VWAP
    cumulative_bid_vol = 0
    cumulative_ask_vol = 0
    bid_vwap_list = []
    ask_vwap_list = []

    table = Table(title=f"Market Depth View - {ticker}", show_header=True, header_style="bold cyan")

    table.add_column("BidVWAP", justify="right")
    table.add_column("Cum Bid Vol", justify="right")
    table.add_column("Bid Volume", justify="right")
    table.add_column("Bid Price", justify="right")
    table.add_column("Ask Price", justify="right")
    table.add_column("Ask Volume", justify="right")
    table.add_column("Cum Ask Vol", justify="right")
    table.add_column("AskVWAP", justify="right")

    for i in range(number_of_data_points):
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
            str(bid_vwap), str(cumulative_bid_vol), str(bid_volume), str(bid_price),
            str(ask_price), str(ask_volume), str(cumulative_ask_vol), str(ask_vwap)
        )
    return table

def generate_signal(ticker: str, price: float, action: str, quantity: int, margin: float =0.0):
    # Generate the market depth table
    market_depth_table = generate_market_depth(ticker)
    console.print(market_depth_table)

    # Convert generator to list
    bid_vwap_list = [float(cell) for cell in market_depth_table.columns[0].cells]
    ask_vwap_list = [float(cell) for cell in market_depth_table.columns[7].cells]

    # For SELL action, we look at bids
    if action == 'SELL':
        bid_vwap_at_quantity = None  # Initialize the variable
        for i, bid_cell in enumerate(market_depth_table.columns[1].cells):  # Iterate through bid levels
            cumulative_bid_vol = int(float(bid_cell))

            if cumulative_bid_vol >= quantity:  # If cumulative volume exceeds the requested quantity
                bid_vwap_at_quantity = bid_vwap_list[i]  # Store the VWAP at this level
                break

        if bid_vwap_at_quantity is None:  # If no level found with sufficient quantity
            bid_vwap_at_quantity = bid_vwap_list[0]  # Best possible VWAP (top bid)

        # Check if the price is favorable for selling
        if price - margin > bid_vwap_at_quantity:
            return (True, bid_vwap_at_quantity)
        return (False, bid_vwap_at_quantity)

    # For BUY action, we look at asks
    elif action == 'BUY':
        ask_vwap_at_quantity = None  # Initialize the variable
        for i, ask_cell in enumerate(market_depth_table.columns[6].cells):  # Iterate through ask levels
            cumulative_ask_vol = int(float(ask_cell))  # Cumulative Ask Volume in column[6]

            if cumulative_ask_vol >= quantity:  # If cumulative volume exceeds the requested quantity
                ask_vwap_at_quantity = ask_vwap_list[i]  # Store the VWAP at this level
                break

        if ask_vwap_at_quantity is None:  # If no level found with sufficient quantity
            ask_vwap_at_quantity = ask_vwap_list[0]  # Best possible VWAP (top ask)

        # Check if the price is favorable for buying
        if price + margin < ask_vwap_at_quantity:
            return (True, ask_vwap_at_quantity)
        return (False, ask_vwap_at_quantity)

    return (False, -1)

# List of tickers you want to generate separate tables for
tickers = ["CRZY", "TAME"]

# Live updating Market Depth tables for each ticker
while True:
    tender_response = []
    # accept no tenders after the mantioned tick value
    if apis.get_current_tick(auth) <= int(os.getenv("T3_TRADE_UNTIL_TICK")):
        tender_response = apis.query_tenders(auth)
        if tender_response:
            print(tender_response)
    for tender in tender_response:
        signal_response = generate_signal(tender["ticker"], tender["price"], tender["action"], tender["quantity"], float(os.getenv("T3_MIN_PROFIT_MARGIN")))
        action = "BUY" if tender["action"] == "BUY" else "SELL"
        print(f"Signal is {signal_response}")
        if signal_response[0]:
            tender_response = apis.post_tender(auth, tender['tender_id'], tender['price'])
            if tender_response["success"]:
                while not apis.is_tender_processed(auth, tender["ticker"]):
                    time.sleep(0.1)
                    print("waiting for tender to be processed")
                asyncio.create_task(apis.stop_loss_square_off_ticker(auth, tender["tender_id"], tender["ticker"], signal_response[1], tender["quantity"], action, loss_percent=0.1, batch_size=5000))             
                apis.instant_square_off_ticker(auth, tender["ticker"])
        else:
            print(f"Tender declined: {apis.decline_tender(auth, tender['tender_id'])}")
    time.sleep(1)