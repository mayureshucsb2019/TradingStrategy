import os
from utility import pretty_print
from vwap_strategy import VWAPStrategy
from dotenv import load_dotenv # type: ignore

# Load environment variables from .env file
load_dotenv()

# # Read values from .env
# auth = {
#     "username": os.getenv("USERNAME"),
#     "password": os.getenv("PASSWORD"),
#     "server": os.getenv("SERVER"),
#     "port": os.getenv("PORT")
# }
# print(auth)
# case_data = apis.query_case_status(auth)
# pretty_print(case_data)
# case_data = apis.query_trader_info(auth)
# pretty_print(case_data)
# case_data = apis.query_trading_limits(auth)
# pretty_print(case_data)

# case_data = apis.query_recent_news(auth)
# pretty_print(case_data)
# case_data = apis.query_assets(auth)
# pretty_print(case_data)
# case_data = apis.query_asset_history(auth)
# pretty_print(case_data)

# case_data = apis.query_securities(auth)
# pretty_print(case_data)
# case_data = apis.query_order_book(auth)
# pretty_print(case_data)
# case_data = apis.query_security_history(auth)
# pretty_print(case_data)

# Example Usage:
vwap = VWAPStrategy(
    ticker="TNX",
    number_of_shares_to_fill=100000,
    number_of_trades=10,
    action="BUY"
)
vwap.start()