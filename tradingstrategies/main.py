import os, sys, time
from utility import pretty_print
from vwap_strategy import VWAPStrategy
from vwap_models import TradeConfig, TradeAction
from models import OrderStatus, OHLCParams
import apis
from dotenv import load_dotenv # type: ignore

# Load environment variables from .env file
load_dotenv()

# Read values from .env
auth = {
    "username": os.getenv("USERNAME"),
    "password": os.getenv("PASSWORD"),
    "server": os.getenv("SERVER"),
    "port": os.getenv("PORT")
}
# print(auth)
# case_data = apis.query_case_status(auth)
# pretty_print(case_data)
# case_data = apis.query_trader_info(auth)
# pretty_print(case_data)
# case_data = apis.query_trading_limits(auth)
# pretty_print(case_data)
# case_data = apis.query_recent_news(auth)
# pretty_print(case_data)

########## NOT WORKING BELOW ASSETS ##########
# case_data = apis.query_assets(auth, "CRZY")
# pretty_print(case_data)
# case_data = apis.query_asset_history(auth)
# pretty_print(case_data)

securities_data = apis.query_securities(auth,"CRZY")
print(securities_data)

# print("Securities book data")
# while True:
#     securities_book_data = apis.query_security_order_book(auth,"CRZY")
#     bids = sorted(securities_book_data["bids"], key=lambda x: x["price"], reverse=True)[:20]  # Top 20 bid levels
#     asks = sorted(securities_book_data["asks"], key=lambda x: x["price"])[:20]

#     cumulative_bid_vol = 0
#     cumulative_ask_vol = 0
#     bid_vwap_list = []
#     ask_vwap_list = []

#     for i in range(len(bids)):        
#         print(bids[0])
#         print(asks[0])
#         print()
#     # securities_data = apis.query_securities(auth, "CRZY")
#     # for x in securities_data:
#     #     print(f"{x['ticker']} {x['position']} {x['last']} {x['bid']} {x['bid_size']} {x['ask']} {x['ask_size']} {x['volume']}\n")
#     # for x in securities_book_data['bids']:
#     #     print(x)
#     # print()
#     time.sleep(1)
# for i, val in securities_book_data['bids']:
#     print(i, val)
# while True:
#     securities_data = apis.query_securities(auth)
#     for x in securities_data:
#     # security_tickers.append(x.ticker)
#         sys.stdout.write(f"{x['ticker']} {x['position']} {x['last']} {x['bid']} {x['bid_size']} {x['ask']} {x['ask_size']} {x['volume']}\n")    
#     sys.stdout.write("\n")    
#     time.sleep(1)
#     sys.stdout.flush()

# security_order_book = apis.query_security_order_book(auth=auth, ticker="CRZY")
# pretty_print(security_order_book)
# case_data = apis.query_orders(auth, OrderStatus.OPEN)
# pretty_print(case_data)
# case_data = apis.query_security_ohlc_history(auth, OHLCParams(ticker="CRZY", period=1,limit=1))
# pretty_print(case_data)

# # Example VWAP Usage:
# config = TradeConfig(
#     username=os.getenv("USERNAME"),  
#     password=os.getenv("PASSWORD"),
#     server=os.getenv("SERVER"),
#     port=int(os.getenv("VWAP_PORT")),  
#     ticker=os.getenv("VWAP_TICKER"),
#     number_of_shares_to_fill=int(os.getenv("VWAP_SHARES_TO_FILL")),
#     number_of_trades=int(os.getenv("VWAP_TRADES")),
#     action=os.getenv("VWAP_TRADE_ACTION")
# )

# vwap = VWAPStrategy(config=config)
# vwap.start()