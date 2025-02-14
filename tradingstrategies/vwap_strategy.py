import apis
import os
from utility import pretty_print
from vwap_model import CaseData
from model import OrderRequest, OrderResponse, OrderStatus
import time
import sys
from dotenv import load_dotenv  # type: ignore

class VWAPStrategy:
    def __init__(self, ticker, number_of_shares_to_fill=100000, number_of_trades=10, action="BUY"):
        # Load environment variables from .env file
        load_dotenv()

        # Authentication details
        self.auth = {
            "username": os.getenv("USERNAME"),
            "password": os.getenv("PASSWORD"),
            "server": os.getenv("SERVER"),
            "port": os.getenv("PORT"),
        }

        # Initialize strategy parameters
        self.ticker = ticker
        self.number_of_shares_to_fill = number_of_shares_to_fill
        self.number_of_trades = number_of_trades
        self.action = action

        # Fetch case data
        case_data = CaseData.model_validate(apis.query_case_status(self.auth))
        self.current_tick = case_data.tick
        self.ticks_per_period = case_data.ticks_per_period

        # Calculate trade size and time between trades
        self.trade_size = self.number_of_shares_to_fill // self.number_of_trades
        self.time_between_trades = int((self.ticks_per_period - self.current_tick) / self.number_of_trades)

        # Adjust if there's only one trade
        if self.time_between_trades <= 1:
            self.number_of_trades = 1
            self.trade_size = self.number_of_shares_to_fill

    def execute_trade(self, trade_index, is_order_detail_allowed=True):
        quantity = self.trade_size
        # For last trade, get left over value, as some might be fractional
        if self.number_of_trades != 1 and trade_index == self.number_of_trades - 1:
            quantity = self.number_of_shares_to_fill - trade_index * self.trade_size
        
        # Order parameters
        order_details = OrderRequest(
            ticker=self.ticker,
            type="MARKET",
            quantity=quantity,
            action=self.action,
            dry_run=0
        )

        # Post order
        OrderResponse.model_validate(apis.post_order(self.auth, order_details))
        print(f"Executed trade {trade_index + 1} for {self.ticker} with {quantity} shares ....... \n")

        # Query order details
        order_detail = apis.query_orders(self.auth, OrderStatus.TRANSACTED)
        if is_order_detail_allowed:
            pretty_print(order_detail)

    def start(self, is_order_detail_allowed=True):
        for i in range(0, self.number_of_trades):
            self.execute_trade(i, is_order_detail_allowed)

            # Sleep before placing the next order (skip sleep after the last trade)
            if i < self.number_of_trades - 1:
                for remaining in range(self.time_between_trades, 0, -1):
                    sys.stdout.write(f"\rWaiting... {remaining} seconds  ")
                    sys.stdout.flush()
                    time.sleep(1)
