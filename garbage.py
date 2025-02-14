# def query_orders(auth: AuthConfig):
#     """Queries all orders."""
#     api_endpoint = f"http://{auth["server"]}:{auth["port"]}/v1/orders"
#     try:
#         headers = make_encoded_header(auth["username"], auth["password"])
#         response = requests.get(api_endpoint, headers=headers)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Error querying orders: {e}")
#         return None


# print("Tick: ", helper.get_current_tick(auth))
# trader_info = apis.query_trader_info(auth)
# pretty_print(trader_info)
# trading_limits = apis.query_trading_limits(auth)
# pretty_print(trading_limits)
# news_data = apis.query_recent_news(auth)
# pretty_print(news_data)
# securities_data = apis.query_securities(auth)
# pretty_print(securities_data)
# securities_book = apis.query_order_book(auth, "TNX")
# pretty_print(securities_book)
# securities_book = apis.query_security_ohlc_history(auth, OHLCParams(ticker=ticker, period=1,limit=1))
# pretty_print(securities_book)
# times_sales = apis.query_time_and_sales(auth, TimeSalesParams(ticker=ticker))
# pretty_print(times_sales)
# order_detail = apis.query_orders(auth, OrderStatus.TRANSACTED)
# pretty_print(order_detail)
# print("Tick: ", helper.get_current_tick(auth))

# import apis
# import os
# from utility import pretty_print
# from vwap_model import CaseData
# from model import OrderRequest, OrderResponse, OrderStatus
# import time
# import sys
# from dotenv import load_dotenv # type: ignore

# # Load environment variables from .env file
# load_dotenv()

# # Read values from .env
# auth = {
#     "username": os.getenv("USERNAME"),
#     "password": os.getenv("PASSWORD"),
#     "server": os.getenv("SERVER"),
#     "port": os.getenv("PORT")
# }

# case_data = CaseData.model_validate(apis.query_case_status(auth))

# TICKER = "TNX"
# NUMBER_OF_SHARES_TO_FILL = 100000
# NUMBER_OF_TRADES = 10
# current_tick = case_data.tick
# ticks_per_period = case_data.ticks_per_period
# trade_size = NUMBER_OF_SHARES_TO_FILL // NUMBER_OF_TRADES
# time_between_trades = int((ticks_per_period-current_tick) / NUMBER_OF_TRADES)

# if time_between_trades <= 1:
#     NUMBER_OF_TRADES = 1
#     trade_size = NUMBER_OF_SHARES_TO_FILL

# for i in range(0, NUMBER_OF_TRADES):
#     quantity = trade_size
#     # for last trade, get left over value, as some might be fractional
#     if NUMBER_OF_TRADES != 1 and i == NUMBER_OF_TRADES-1:
#         quantity = NUMBER_OF_SHARES_TO_FILL - i * trade_size
#     # Order parameters
#     order_details = OrderRequest(
#         ticker=TICKER,
#         type="MARKET",
#         quantity=quantity,
#         action="BUY",
#         dry_run=0  # Change to 1 for simulation
#     )
#     order_transaction = OrderResponse.model_validate(apis.post_order(auth, order_details))
#     print(f"Exectuted trade {i+1} for {TICKER} with {quantity} shares ....... \n")
#     pretty_print(order_transaction)
#     order_detail = apis.query_orders(auth, OrderStatus.TRANSACTED)
#     pretty_print(order_detail)
#     # Sleep before placing the next order (skip sleep after the last trade)
#     if i < NUMBER_OF_TRADES-1:
#         for remaining in range(time_between_trades, 0, -1):
#             sys.stdout.write(f"\rWaiting... {remaining} seconds  ")
#             sys.stdout.flush()
#             time.sleep(1)
#         print("\rExecuting next trade...  ")

