"""
Kaspa (KAS) Cross-Exchange Arbitrage Strategy
Using Hummingbot V2 Strategy Framework with ArbitrageExecutor

This script monitors price discrepancies for KAS across multiple CEX exchanges
and executes arbitrage trades when profitable opportunities arise.

Supported exchanges (that support KAS):
- Binance (futures only - check availability)
- KuCoin
- Kraken  
- Bybit
- MEXC
- Gate.io
- Bitget
"""

import logging
from decimal import Decimal
from typing import Dict, List, Optional

from hummingbot.client.config.config_helpers import ClientConfigAdapter
from hummingbot.connector.connector_base import ConnectorBase
from hummingbot.core.data_type.common import OrderType, TradeType
from hummingbot.data_feed.candles_feed.candles_factory import CandlesConfig
from hummingbot.strategy.script_strategy_base import ScriptStrategyBase
from hummingbot.strategy_v2.executors.arbitrage_executor.arbitrage_executor import ArbitrageExecutor
from hummingbot.strategy_v2.executors.arbitrage_executor.data_types import ArbitrageConfig
from hummingbot.strategy_v2.models.executors import CloseType


class KaspaArbitrageStrategy(ScriptStrategyBase):
    """
    Kaspa arbitrage strategy that monitors multiple exchanges and executes
    trades when price discrepancies exceed the minimum profitability threshold.
    """
    
    # ====== CONFIGURATION PARAMETERS ======
    
    # Exchange pairs to monitor for arbitrage
    # Format: [(exchange1, exchange2), ...]
    exchange_pairs = [
        ("kucoin", "kraken"),
        ("kucoin", "bybit"),
        ("mexc", "gate_io"),
        ("bitget", "kucoin"),
        # Add more pairs as needed
    ]
    
    # Trading pair (same across all exchanges)
    trading_pair = "KAS-USDT"  # Adjust based on exchange availability
    
    # Minimum profitability to execute arbitrage (in percentage)
    # Example: 0.003 = 0.3% minimum profit
    min_profitability = Decimal("0.005")  # 0.5%
    
    # Order amount in base asset (KAS)
    order_amount = Decimal("100")  # Adjust based on your capital
    
    # Maximum number of concurrent arbitrage positions
    max_concurrent_arbitrages = 3
    
    # Time delay between arbitrage checks (in seconds)
    check_interval = 5.0
    
    # Slippage buffer for each exchange (to account for price movement)
    # Higher values = more conservative pricing
    slippage_buffers = {
        "kucoin": Decimal("0.001"),    # 0.1%
        "kraken": Decimal("0.001"),
        "bybit": Decimal("0.001"),
        "mexc": Decimal("0.0015"),     # 0.15% (adjust based on liquidity)
        "gate_io": Decimal("0.001"),
        "bitget": Decimal("0.001"),
    }
    
    # ====== INTERNAL STATE ======
    
    markets = {}  # Will be populated with exchange connectors
    active_executors: Dict[str, ArbitrageExecutor] = {}
    last_check_timestamp = 0
    
    def __init__(self, connectors: Dict[str, ConnectorBase]):
        super().__init__(connectors)
        self.markets = connectors
        
    def on_tick(self):
        """
        Main strategy logic executed every tick.
        Checks for arbitrage opportunities and executes trades.
        """
        current_timestamp = self.current_timestamp
        
        # Check if enough time has passed since last check
        if current_timestamp - self.last_check_timestamp < self.check_interval:
            return
            
        self.last_check_timestamp = current_timestamp
        
        # Clean up completed executors
        self.clean_up_executors()
        
        # Check if we can open new arbitrage positions
        if len(self.active_executors) >= self.max_concurrent_arbitrages:
            self.logger().info(f"Maximum concurrent arbitrages reached ({self.max_concurrent_arbitrages})")
            return
        
        # Check for arbitrage opportunities
        opportunities = self.find_arbitrage_opportunities()
        
        if opportunities:
            self.logger().info(f"Found {len(opportunities)} arbitrage opportunities")
            for opp in opportunities[:self.max_concurrent_arbitrages - len(self.active_executors)]:
                self.execute_arbitrage(opp)
        
    def find_arbitrage_opportunities(self) -> List[Dict]:
        """
        Scans all exchange pairs for profitable arbitrage opportunities.
        
        Returns:
            List of arbitrage opportunity dictionaries
        """
        opportunities = []
        
        for exchange1, exchange2 in self.exchange_pairs:
            # Check if both exchanges are connected
            if exchange1 not in self.markets or exchange2 not in self.markets:
                self.logger().warning(f"Exchange pair {exchange1}/{exchange2} not connected")
                continue
            
            connector1 = self.markets[exchange1]
            connector2 = self.markets[exchange2]
            
            # Get order books
            try:
                # Get best bid and ask prices
                bid_price_1 = connector1.get_price(self.trading_pair, False)  # Sell price
                ask_price_1 = connector1.get_price(self.trading_pair, True)   # Buy price
                
                bid_price_2 = connector2.get_price(self.trading_pair, False)
                ask_price_2 = connector2.get_price(self.trading_pair, True)
                
                if not all([bid_price_1, ask_price_1, bid_price_2, ask_price_2]):
                    continue
                
                # Calculate potential profit for both directions
                # Direction 1: Buy on exchange1, sell on exchange2
                profit_1 = self.calculate_profit(
                    buy_price=ask_price_1,
                    sell_price=bid_price_2,
                    buy_exchange=exchange1,
                    sell_exchange=exchange2
                )
                
                # Direction 2: Buy on exchange2, sell on exchange1
                profit_2 = self.calculate_profit(
                    buy_price=ask_price_2,
                    sell_price=bid_price_1,
                    buy_exchange=exchange2,
                    sell_exchange=exchange1
                )
                
                # Check if either direction is profitable
                if profit_1 >= self.min_profitability:
                    opportunities.append({
                        "buy_exchange": exchange1,
                        "sell_exchange": exchange2,
                        "buy_price": ask_price_1,
                        "sell_price": bid_price_2,
                        "profit_pct": profit_1,
                        "amount": self.order_amount
                    })
                    self.logger().info(
                        f"Arbitrage opportunity: Buy {exchange1} @ {ask_price_1}, "
                        f"Sell {exchange2} @ {bid_price_2}, Profit: {profit_1:.2%}"
                    )
                
                if profit_2 >= self.min_profitability:
                    opportunities.append({
                        "buy_exchange": exchange2,
                        "sell_exchange": exchange1,
                        "buy_price": ask_price_2,
                        "sell_price": bid_price_1,
                        "profit_pct": profit_2,
                        "amount": self.order_amount
                    })
                    self.logger().info(
                        f"Arbitrage opportunity: Buy {exchange2} @ {ask_price_2}, "
                        f"Sell {exchange1} @ {bid_price_1}, Profit: {profit_2:.2%}"
                    )
                    
            except Exception as e:
                self.logger().error(f"Error checking {exchange1}/{exchange2}: {str(e)}")
                
        return opportunities
    
    def calculate_profit(
        self,
        buy_price: Decimal,
        sell_price: Decimal,
        buy_exchange: str,
        sell_exchange: str
    ) -> Decimal:
        """
        Calculate net profitability accounting for fees and slippage.
        
        Args:
            buy_price: Price to buy at
            sell_price: Price to sell at
            buy_exchange: Exchange to buy from
            sell_exchange: Exchange to sell on
            
        Returns:
            Net profit percentage (after fees and slippage)
        """
        # Apply slippage buffers
        buy_slippage = self.slippage_buffers.get(buy_exchange, Decimal("0.001"))
        sell_slippage = self.slippage_buffers.get(sell_exchange, Decimal("0.001"))
        
        adjusted_buy_price = buy_price * (Decimal("1") + buy_slippage)
        adjusted_sell_price = sell_price * (Decimal("1") - sell_slippage)
        
        # Get trading fees (maker/taker)
        # Most exchanges charge ~0.1% for taker orders
        buy_fee = Decimal("0.001")  # 0.1% - adjust based on your fee tier
        sell_fee = Decimal("0.001")
        
        # Calculate gross profit
        gross_profit = (adjusted_sell_price - adjusted_buy_price) / adjusted_buy_price
        
        # Subtract fees
        net_profit = gross_profit - buy_fee - sell_fee
        
        return net_profit
    
    def execute_arbitrage(self, opportunity: Dict):
        """
        Execute an arbitrage trade based on the opportunity.
        
        Args:
            opportunity: Dictionary containing arbitrage details
        """
        try:
            buy_exchange = opportunity["buy_exchange"]
            sell_exchange = opportunity["sell_exchange"]
            amount = opportunity["amount"]
            
            # Check balances before executing
            if not self.check_sufficient_balance(buy_exchange, sell_exchange, amount):
                self.logger().warning(
                    f"Insufficient balance for arbitrage between {buy_exchange} and {sell_exchange}"
                )
                return
            
            # Create arbitrage executor
            arbitrage_config = ArbitrageConfig(
                buying_market=self.markets[buy_exchange],
                selling_market=self.markets[sell_exchange],
                order_amount=amount,
                min_profitability=self.min_profitability,
            )
            
            executor = ArbitrageExecutor(
                strategy=self,
                arbitrage_config=arbitrage_config,
                update_interval=1.0
            )
            
            # Store executor
            executor_id = f"{buy_exchange}_{sell_exchange}_{self.current_timestamp}"
            self.active_executors[executor_id] = executor
            
            # Start executor
            executor.start()
            
            self.logger().info(
                f"Started arbitrage executor {executor_id}: "
                f"Buy {buy_exchange}, Sell {sell_exchange}, "
                f"Amount: {amount} KAS, Expected profit: {opportunity['profit_pct']:.2%}"
            )
            
        except Exception as e:
            self.logger().error(f"Error executing arbitrage: {str(e)}")
    
    def check_sufficient_balance(
        self,
        buy_exchange: str,
        sell_exchange: str,
        amount: Decimal
    ) -> bool:
        """
        Check if there's sufficient balance on both exchanges.
        
        Args:
            buy_exchange: Exchange to buy from (needs quote currency)
            sell_exchange: Exchange to sell on (needs base currency)
            amount: Amount of base currency (KAS) to trade
            
        Returns:
            True if sufficient balance exists on both exchanges
        """
        try:
            # Get base and quote currencies
            base, quote = self.trading_pair.split("-")
            
            # Check quote balance on buying exchange
            buy_connector = self.markets[buy_exchange]
            quote_balance = buy_connector.get_available_balance(quote)
            
            # Estimate required quote amount (with buffer)
            estimated_price = buy_connector.get_price(self.trading_pair, True)
            required_quote = amount * estimated_price * Decimal("1.01")  # 1% buffer
            
            if quote_balance < required_quote:
                self.logger().warning(
                    f"Insufficient {quote} balance on {buy_exchange}: "
                    f"{quote_balance} < {required_quote}"
                )
                return False
            
            # Check base balance on selling exchange
            sell_connector = self.markets[sell_exchange]
            base_balance = sell_connector.get_available_balance(base)
            
            if base_balance < amount:
                self.logger().warning(
                    f"Insufficient {base} balance on {sell_exchange}: "
                    f"{base_balance} < {amount}"
                )
                return False
            
            return True
            
        except Exception as e:
            self.logger().error(f"Error checking balances: {str(e)}")
            return False
    
    def clean_up_executors(self):
        """Remove completed or failed executors from active list."""
        completed_ids = []
        
        for executor_id, executor in self.active_executors.items():
            if executor.is_closed:
                close_type = executor.close_type
                self.logger().info(
                    f"Executor {executor_id} closed with type: {close_type}"
                )
                completed_ids.append(executor_id)
                
                # Log performance
                if close_type == CloseType.COMPLETED:
                    self.logger().info(f"Arbitrage completed successfully: {executor_id}")
                elif close_type == CloseType.FAILED:
                    self.logger().warning(f"Arbitrage failed: {executor_id}")
        
        # Remove completed executors
        for executor_id in completed_ids:
            del self.active_executors[executor_id]
    
    def format_status(self) -> str:
        """
        Returns formatted status string for the strategy.
        """
        status = []
        status.append(f"\n{'=' * 60}")
        status.append(f"Kaspa Arbitrage Strategy Status")
        status.append(f"{'=' * 60}")
        status.append(f"Trading Pair: {self.trading_pair}")
        status.append(f"Min Profitability: {self.min_profitability:.2%}")
        status.append(f"Order Amount: {self.order_amount} KAS")
        status.append(f"Active Arbitrages: {len(self.active_executors)}/{self.max_concurrent_arbitrages}")
        
        # Show connected exchanges
        status.append(f"\nConnected Exchanges:")
        for exchange in self.markets.keys():
            status.append(f"  - {exchange}")
        
        # Show active executors
        if self.active_executors:
            status.append(f"\nActive Arbitrage Positions:")
            for executor_id, executor in self.active_executors.items():
                status.append(f"  - {executor_id}: {executor.executor_status}")
        
        status.append(f"{'=' * 60}\n")
        return "\n".join(status)


# ====== CONFIGURATION HELPER ======

def create_kaspa_arbitrage_config():
    """
    Helper function to create configuration for the Kaspa arbitrage strategy.
    Adjust these parameters based on your needs.
    """
    config = {
        "exchange_pairs": [
            ("kucoin", "kraken"),
            ("kucoin", "bybit"),
            ("mexc", "gate_io"),
        ],
        "trading_pair": "KAS-USDT",
        "min_profitability": Decimal("0.005"),  # 0.5%
        "order_amount": Decimal("100"),
        "max_concurrent_arbitrages": 3,
        "check_interval": 5.0,
        "slippage_buffers": {
            "kucoin": Decimal("0.001"),
            "kraken": Decimal("0.001"),
            "bybit": Decimal("0.001"),
            "mexc": Decimal("0.0015"),
            "gate_io": Decimal("0.001"),
            "bitget": Decimal("0.001"),
        }
    }
    return config
