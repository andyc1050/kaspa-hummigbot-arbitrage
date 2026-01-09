# Kaspa Arbitrage - Simple Configuration (Using Built-in Strategy)

## Quick Start with AMM Arb Strategy

This is the simplest way to run Kaspa arbitrage using Hummingbot's built-in strategy.

### Step 1: Start Hummingbot

```bash
# If using Docker
docker run -it --name hummingbot hummingbot/hummingbot:latest

# If using source
./start
```

### Step 2: Connect Exchanges

```bash
# Connect to your first exchange (e.g., KuCoin)
connect kucoin

# Connect to your second exchange (e.g., Kraken)
connect kraken
```

### Step 3: Create Strategy

```bash
create
```

When prompted:

```
What is your market making strategy?
>>> amm_arb

On which exchange would you like to make (market 1)?
>>> kucoin

What is the trading pair on kucoin?
>>> KAS-USDT

On which exchange would you like to make (market 2)?
>>> kraken

What is the trading pair on kraken?
>>> KAS-USDT

What is the amount of [base_asset] per order?
>>> 100

What is the minimum profitability for you to make a trade?
>>> 0.005

What is the slippage buffer for market 1?
>>> 0.001

What is the slippage buffer for market 2?
>>> 0.001

Do you want to enable concurrent orders submission?
>>> Yes
```

### Step 4: Start Strategy

```bash
start
```

---

## Configuration File Example

If you prefer to create the configuration file manually:

**Location:** `conf/conf_amm_arb_kas_kucoin_kraken.yml`

```yaml
##############################
# Kaspa Arbitrage Strategy
# Markets: KuCoin <-> Kraken
##############################

strategy: amm_arb

# Exchange 1 (KuCoin)
connector_1: kucoin
market_1: KAS-USDT

# Exchange 2 (Kraken)
connector_2: kraken
market_2: KAS-USDT

# Order Configuration
order_amount: 100.0

# Minimum profit to execute trade (0.5%)
min_profitability: 0.005

# Slippage buffers (0.1% each)
market_1_slippage_buffer: 0.001
market_2_slippage_buffer: 0.001

# Submit orders concurrently for faster execution
concurrent_orders_submission: true

# Optional: Maximum order age before cancelling
# order_refresh_time: 30.0

# Optional: Enable this to only check for arbitrage without executing
# debug_mode: false
```

### Import Configuration

```bash
import conf_amm_arb_kas_kucoin_kraken.yml
start
```

---

## Multiple Configuration Files

Create separate configs for different exchange pairs:

### KuCoin <-> Bybit

**File:** `conf_amm_arb_kas_kucoin_bybit.yml`

```yaml
strategy: amm_arb
connector_1: kucoin
market_1: KAS-USDT
connector_2: bybit
market_2: KAS-USDT
order_amount: 100.0
min_profitability: 0.005
market_1_slippage_buffer: 0.001
market_2_slippage_buffer: 0.001
concurrent_orders_submission: true
```

### MEXC <-> Gate.io

**File:** `conf_amm_arb_kas_mexc_gate.yml`

```yaml
strategy: amm_arb
connector_1: mexc
market_1: KAS-USDT
connector_2: gate_io
market_2: KAS-USDT
order_amount: 100.0
min_profitability: 0.005
market_1_slippage_buffer: 0.0015
market_2_slippage_buffer: 0.001
concurrent_orders_submission: true
```

---

## Running Multiple Instances

To run arbitrage across multiple exchange pairs simultaneously:

### Option 1: Multiple Docker Containers

```bash
# KuCoin <-> Kraken
docker run -it --name hummingbot-kas-kucoin-kraken \
  -v "$(pwd)/conf1:/conf" \
  hummingbot/hummingbot:latest

# KuCoin <-> Bybit  
docker run -it --name hummingbot-kas-kucoin-bybit \
  -v "$(pwd)/conf2:/conf" \
  hummingbot/hummingbot:latest

# MEXC <-> Gate.io
docker run -it --name hummingbot-kas-mexc-gate \
  -v "$(pwd)/conf3:/conf" \
  hummingbot/hummingbot:latest
```

### Option 2: Screen/Tmux Sessions (Linux)

```bash
# Session 1: KuCoin <-> Kraken
screen -S kas-kucoin-kraken
./start
import conf_amm_arb_kas_kucoin_kraken.yml
start
# Press Ctrl+A, then D to detach

# Session 2: KuCoin <-> Bybit
screen -S kas-kucoin-bybit
./start
import conf_amm_arb_kas_kucoin_bybit.yml
start
# Press Ctrl+A, then D to detach

# List sessions
screen -ls

# Reattach to session
screen -r kas-kucoin-kraken
```

---

## Command Reference

### Basic Commands

```bash
# View current status
status

# Check balances
balance

# View trade history
history

# Stop strategy
stop

# Exit Hummingbot
exit
```

### Advanced Commands

```bash
# View configuration
config

# Change configuration parameter
config min_profitability 0.003

# Export trade history
export_trades

# View performance
performance

# Show rate oracle prices
rate

# Paper trading mode (testing)
paper_trading
```

---

## Parameter Tuning Guide

### min_profitability

| Value | Description | Recommendation |
|-------|-------------|----------------|
| 0.002 (0.2%) | Very aggressive | High-volume pairs only |
| 0.003 (0.3%) | Aggressive | Good liquidity required |
| 0.005 (0.5%) | Moderate | **Recommended for beginners** |
| 0.008 (0.8%) | Conservative | Lower frequency trades |
| 0.010 (1.0%) | Very conservative | Rare but high profit |

### order_amount

Start small and scale up:

1. **Testing Phase:** 50 KAS ($2.50 at $0.05/KAS)
2. **Initial Production:** 100 KAS ($5.00)
3. **Scaling Phase:** 200-500 KAS ($10-25)
4. **Full Production:** 1000+ KAS ($50+)

### slippage_buffer

Adjust based on exchange liquidity:

| Exchange | Recommended Buffer | Notes |
|----------|-------------------|-------|
| KuCoin | 0.0010 (0.1%) | High liquidity |
| Kraken | 0.0010 (0.1%) | High liquidity |
| Bybit | 0.0010 (0.1%) | Good liquidity |
| MEXC | 0.0015 (0.15%) | Medium liquidity |
| Gate.io | 0.0010 (0.1%) | Good liquidity |
| Bitget | 0.0012 (0.12%) | Medium liquidity |

---

## Monitoring Scripts

### Check All Running Instances (Bash)

Create file: `check_status.sh`

```bash
#!/bin/bash

echo "=== Hummingbot KAS Arbitrage Status ==="
echo ""

# Check KuCoin <-> Kraken
echo "1. KuCoin <-> Kraken:"
screen -S kas-kucoin-kraken -X stuff "status^M"
sleep 2

# Check KuCoin <-> Bybit
echo "2. KuCoin <-> Bybit:"
screen -S kas-kucoin-bybit -X stuff "status^M"
sleep 2

# Check MEXC <-> Gate.io
echo "3. MEXC <-> Gate.io:"
screen -S kas-mexc-gate -X stuff "status^M"

echo ""
echo "=== End of Status Check ==="
```

```bash
chmod +x check_status.sh
./check_status.sh
```

### Performance Monitor (Python)

Create file: `monitor_performance.py`

```python
#!/usr/bin/env python3
"""
Monitor Hummingbot KAS arbitrage performance
"""

import os
import re
from datetime import datetime

def parse_log_file(log_path):
    """Parse Hummingbot log file for trade data"""
    trades = []
    
    with open(log_path, 'r') as f:
        for line in f:
            # Look for arbitrage execution lines
            if 'arbitrage' in line.lower() and 'profit' in line.lower():
                # Extract profit information
                # This is a simplified parser - adjust based on actual log format
                trades.append(line.strip())
    
    return trades

def calculate_stats(trades):
    """Calculate performance statistics"""
    total_trades = len(trades)
    
    print(f"Total Arbitrage Trades: {total_trades}")
    print(f"Log Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Add more sophisticated parsing here based on your needs

if __name__ == "__main__":
    log_dir = "logs"  # Adjust path as needed
    log_file = os.path.join(log_dir, "hummingbot_logs.log")
    
    if os.path.exists(log_file):
        trades = parse_log_file(log_file)
        calculate_stats(trades)
    else:
        print(f"Log file not found: {log_file}")
```

---

## Alerts and Notifications

### Telegram Alerts (Optional)

If you want to receive notifications:

1. Create a Telegram bot via @BotFather
2. Get your bot token and chat ID
3. Configure in Hummingbot:

```bash
# In Hummingbot
telegram_enabled
telegram_token YOUR_BOT_TOKEN
telegram_chat_id YOUR_CHAT_ID
```

Hummingbot will send you notifications for:
- Strategy start/stop
- Order fills
- Errors and warnings

---

## Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| "Trading pair not found" | Verify KAS-USDT is available on exchange |
| "Insufficient balance" | Add more USDT and KAS to exchanges |
| "API key invalid" | Check API key permissions and regenerate if needed |
| "Rate limit exceeded" | Reduce check frequency or upgrade API tier |
| "No arbitrage opportunities" | Lower min_profitability or add more pairs |
| "Orders not filling" | Increase slippage_buffer |
| "High failure rate" | Check internet stability and reduce order_amount |

---

## Example Session

Here's what a typical session looks like:

```bash
$ docker run -it --name hummingbot hummingbot/hummingbot:latest

Welcome to Hummingbot!

>>> connect kucoin
Enter your KuCoin API key: ****
Enter your KuCoin secret key: ****
Enter your KuCoin passphrase: ****

You are now connected to kucoin.

>>> connect kraken
Enter your Kraken API key: ****
Enter your Kraken secret key: ****

You are now connected to kraken.

>>> create
What is your market making strategy?
>>> amm_arb

[Configuration prompts...]

>>> start
Strategy started.

>>> status
╔════════════════════════════════════════╗
║     KAS Arbitrage Status              ║
╠════════════════════════════════════════╣
║ Markets: kucoin - kraken              ║
║ Trading Pair: KAS-USDT                ║
║ Min Profitability: 0.50%              ║
║ Order Amount: 100 KAS                 ║
║                                       ║
║ Arbitrage opportunities: 3            ║
║ Trades today: 12                      ║
║ Profit today: $42.50                  ║
╚════════════════════════════════════════╝

[Opportunity detected] Profitable arbitrage found!
Buy kucoin @ 0.05120, Sell kraken @ 0.05187, Profit: 1.31%
[Order submitted] Buy order submitted on kucoin
[Order submitted] Sell order submitted on kraken
[Order filled] Buy order filled: 100 KAS @ 0.05120
[Order filled] Sell order filled: 100 KAS @ 0.05187
[Arbitrage complete] Net profit: $0.65 (1.27% after fees)
```

---

## Next Steps

1. **Start with paper trading**
   ```bash
   paper_trading
   ```

2. **Test with small amounts** ($50-100)

3. **Monitor for 24-48 hours**

4. **Gradually increase capital** if profitable

5. **Optimize parameters** based on results

6. **Add more exchange pairs** to increase opportunities

---

## Useful Links

- [AMM Arb Strategy Docs](https://docs.hummingbot.org/strategies/amm-arb/)
- [Exchange Connectors](https://docs.hummingbot.org/exchanges/)
- [Hummingbot Discord](https://discord.gg/hummingbot)
- [Kaspa Resources](https://www.kaspa.org)

---

**Remember: Start small, test thoroughly, and only scale up once you've verified the strategy works for you!**
