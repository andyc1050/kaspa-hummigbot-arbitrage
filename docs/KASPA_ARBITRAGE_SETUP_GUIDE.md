# Kaspa Arbitrage Strategy - Setup Guide

## Overview

This guide will help you set up and run a market making arbitrage algorithm for Kaspa (KAS) using Hummingbot. The strategy monitors price discrepancies across multiple centralized exchanges and executes profitable arbitrage trades automatically.

## Prerequisites

### 1. System Requirements
- Docker installed (recommended) OR
- Python 3.10+ for source installation
- Minimum 4GB RAM
- Stable internet connection

### 2. Exchange Accounts

You need accounts on at least 2 exchanges that support KAS trading:

**Supported by both Hummingbot AND KAS:**
- ✅ KuCoin (KAS/USDT)
- ✅ Kraken (KAS/USD, KAS/USDT)
- ✅ Bybit (KAS/USDT)
- ✅ MEXC (KAS/USDT)
- ✅ Gate.io (KAS/USDT)
- ✅ Bitget (KAS/USDT)

**Note:** Binance has KAS futures but check current availability.

### 3. API Keys

For each exchange you plan to use:
1. Enable 2FA on your account
2. Create API keys with trading permissions
3. Whitelist your IP address (recommended for security)
4. Save API key and secret securely

### 4. Initial Capital

Required capital depends on your strategy:
- Minimum recommended: $500-1000 per exchange
- Split evenly across exchanges (50% USDT, 50% KAS)
- More capital = more arbitrage opportunities

---

## Installation

### Option 1: Docker (Recommended)

```bash
# Pull the latest Hummingbot image
docker pull hummingbot/hummingbot:latest

# Create a directory for Hummingbot files
mkdir hummingbot_files
cd hummingbot_files

# Create directories for config and scripts
mkdir -p conf scripts logs

# Download the Kaspa arbitrage script
# (Place kaspa_arbitrage_v2.py in the scripts directory)

# Run Hummingbot
docker run -it \
  --name hummingbot \
  --network host \
  -v "$(pwd)/conf:/conf" \
  -v "$(pwd)/scripts:/scripts" \
  -v "$(pwd)/logs:/logs" \
  hummingbot/hummingbot:latest
```

### Option 2: Source Installation

```bash
# Clone Hummingbot repository
git clone https://github.com/hummingbot/hummingbot.git
cd hummingbot

# Install dependencies
./install

# Activate conda environment
conda activate hummingbot

# Compile
./compile

# Start Hummingbot
./start
```

---

## Configuration Steps

### Step 1: Connect to Exchanges

Inside Hummingbot terminal:

```bash
# Connect to KuCoin
connect kucoin

# Connect to Kraken
connect kraken

# Connect to Bybit (optional)
connect bybit

# Connect to MEXC (optional)
connect mexc

# Connect to Gate.io (optional)
connect gate_io

# Connect to Bitget (optional)
connect bitget
```

For each exchange, you'll be prompted for:
- API Key
- Secret Key
- Additional parameters (varies by exchange)

### Step 2: Verify Connections

```bash
# Check balances on all exchanges
balance

# Verify trading pair is available
# This should show KAS balance on each connected exchange
```

### Step 3: Configure the Strategy

Edit the `kaspa_arbitrage_v2.py` file to customize:

```python
# Key parameters to adjust:

# Exchange pairs to monitor
exchange_pairs = [
    ("kucoin", "kraken"),      # Monitor KuCoin vs Kraken
    ("kucoin", "bybit"),        # Monitor KuCoin vs Bybit
    ("mexc", "gate_io"),        # Monitor MEXC vs Gate.io
]

# Minimum profit threshold (0.5% = 0.005)
min_profitability = Decimal("0.005")

# Order size in KAS
order_amount = Decimal("100")  # Start small!

# Maximum concurrent arbitrage positions
max_concurrent_arbitrages = 3

# How often to check for opportunities (seconds)
check_interval = 5.0
```

### Step 4: Place the Script

```bash
# Copy script to Hummingbot scripts directory
# For Docker: Place in ./scripts/
# For Source: Place in hummingbot/scripts/
```

### Step 5: Run the Strategy

In Hummingbot terminal:

```bash
# Import the script
import kaspa_arbitrage_v2

# Start the strategy
start
```

---

## Strategy Parameters Explained

### Core Parameters

**exchange_pairs**
- List of exchange pairs to monitor
- Format: `[("exchange1", "exchange2"), ...]`
- Start with 2-3 pairs, add more as you gain experience

**min_profitability**
- Minimum profit percentage required to execute trade
- Recommended: 0.3% - 0.5% (0.003 - 0.005)
- Lower = more trades but lower profit per trade
- Higher = fewer trades but higher profit per trade

**order_amount**
- Amount of KAS per arbitrage trade
- Start small (50-100 KAS) for testing
- Increase gradually as strategy proves profitable

**max_concurrent_arbitrages**
- Maximum number of simultaneous arbitrage positions
- Recommended: 2-3 for beginners
- More positions = more capital required

**check_interval**
- How often to scan for opportunities (seconds)
- Recommended: 3-5 seconds
- Lower = faster detection but more API calls

### Slippage Buffers

```python
slippage_buffers = {
    "kucoin": Decimal("0.001"),    # 0.1%
    "kraken": Decimal("0.001"),    # 0.1%
    "bybit": Decimal("0.001"),     # 0.1%
    "mexc": Decimal("0.0015"),     # 0.15%
    "gate_io": Decimal("0.001"),   # 0.1%
    "bitget": Decimal("0.001"),    # 0.1%
}
```

Adjust based on:
- Exchange liquidity (lower liquidity = higher buffer)
- Your risk tolerance
- Historical price movement during execution

---

## Risk Management

### 1. Capital Allocation

**Conservative Approach:**
```
Total Capital: $2,000
- Exchange 1: $1,000 (50% USDT, 50% KAS)
- Exchange 2: $1,000 (50% USDT, 50% KAS)
```

**Aggressive Approach:**
```
Total Capital: $5,000
- Distributed across 3-4 exchanges
- 60% in high-volume exchanges
- 40% in low-volume exchanges
```

### 2. Position Sizing

- Never risk more than 1-2% of total capital per trade
- Start with smaller positions (50-100 KAS)
- Scale up gradually based on performance

### 3. Exchange Risk

- Don't hold all funds on one exchange
- Use only reputable exchanges
- Enable withdrawal whitelist
- Use 2FA and API IP whitelisting

### 4. Network Risk

- Arbitrage requires fast execution
- Use VPS or stable internet connection
- Monitor for high latency issues

---

## Monitoring and Optimization

### Real-time Monitoring

```bash
# Check strategy status
status

# View active positions
# (Shows in the strategy status output)

# Check recent trades
history

# View detailed logs
# Check logs directory for detailed execution logs
```

### Performance Metrics to Track

1. **Total Profit/Loss**
   - Track daily, weekly, monthly returns
   - Calculate against initial capital

2. **Win Rate**
   - Percentage of profitable arbitrage trades
   - Target: >70%

3. **Average Profit per Trade**
   - Should exceed transaction costs
   - Target: >0.3%

4. **Execution Speed**
   - Time from detection to execution
   - Target: <10 seconds

5. **Failed Trades**
   - Why did they fail?
   - Insufficient balance?
   - Price moved too quickly?

### Optimization Tips

1. **Adjust min_profitability**
   - If too many failed trades → increase threshold
   - If too few opportunities → decrease threshold

2. **Optimize exchange pairs**
   - Track which pairs are most profitable
   - Remove underperforming pairs
   - Add new pairs with high volume differences

3. **Tune slippage buffers**
   - Too high → missing opportunities
   - Too low → failed executions

4. **Order amount**
   - Larger orders may move the market
   - Smaller orders may not be worth the fees

---

## Troubleshooting

### Common Issues

**Issue: "Insufficient balance"**
- Solution: Ensure both exchanges have adequate KAS and USDT
- Rebalance if one exchange runs low

**Issue: "No opportunities found"**
- Solution 1: Lower min_profitability threshold
- Solution 2: Add more exchange pairs
- Solution 3: Check if trading pair is available on exchanges

**Issue: "Orders not executing"**
- Solution 1: Check API key permissions
- Solution 2: Verify trading pair format (KAS-USDT vs KAS/USDT)
- Solution 3: Check exchange status (maintenance, trading halted)

**Issue: "High failure rate"**
- Solution 1: Increase slippage buffers
- Solution 2: Reduce order amount
- Solution 3: Improve internet connection speed

**Issue: "API rate limit errors"**
- Solution 1: Increase check_interval
- Solution 2: Reduce number of exchange pairs
- Solution 3: Upgrade to higher API tier if available

### Logs and Debugging

```bash
# View logs in real-time
tail -f logs/hummingbot_logs.log

# Search for errors
grep ERROR logs/hummingbot_logs.log

# Check specific arbitrage execution
grep "arbitrage" logs/hummingbot_logs.log
```

---

## Advanced: Alternative Strategy (V1 AMM Arb)

If you prefer the simpler V1 strategy template:

```bash
# In Hummingbot terminal
create

# Select strategy
amm_arb

# Follow prompts to configure:
# - First connector: kucoin
# - Trading pair: KAS-USDT
# - Second connector: kraken
# - Trading pair: KAS-USDT
# - Order amount: 100
# - Min profitability: 0.005 (0.5%)
```

---

## Future: DEX Integration

When Kaspa DEX support becomes available in Hummingbot:

1. **Check for Gateway support**
   - Monitor Hummingbot updates
   - Look for Kaspa DEX connectors

2. **Gateway setup required**
   - Install Hummingbot Gateway
   - Connect wallet (MetaMask, Ledger)
   - Configure blockchain RPC endpoints

3. **Advantages of CEX-DEX arbitrage**
   - Often larger price discrepancies
   - Less competition
   - More opportunities

4. **Additional considerations**
   - Gas fees (blockchain transactions)
   - Longer execution times
   - Smart contract risk

---

## Best Practices

### Security

1. **API Keys**
   - Use separate API keys for Hummingbot
   - Limit permissions (trading only, no withdrawal)
   - Rotate keys periodically
   - Enable IP whitelist

2. **System Security**
   - Use dedicated machine/VPS
   - Keep system updated
   - Use firewall
   - Regular backups of config files

3. **Operational Security**
   - Never share API keys
   - Don't run unverified scripts
   - Review all code before running
   - Test with small amounts first

### Testing

1. **Paper Trading**
   ```bash
   # Enable paper trading mode
   paper_trading
   ```
   - Test strategy without real funds
   - Verify logic works correctly
   - Tune parameters

2. **Small Capital Test**
   - Start with $100-200
   - Run for 24-48 hours
   - Analyze results
   - Scale up if profitable

3. **Gradual Scaling**
   - Week 1: $200
   - Week 2: $500 (if profitable)
   - Week 3: $1,000 (if consistently profitable)
   - Continue scaling based on performance

---

## Performance Expectations

### Realistic Targets

**Conservative Strategy (0.5% min profit):**
- Trades per day: 5-15
- Average profit per trade: 0.3-0.5%
- Daily return: 1.5-7.5%
- Monthly return: 45-225% (compound)

**Aggressive Strategy (0.3% min profit):**
- Trades per day: 15-30
- Average profit per trade: 0.2-0.4%
- Daily return: 3-12%
- Monthly return: 90-360% (compound)

**Note:** These are estimates. Actual results depend on:
- Market conditions
- Competition from other arbitrageurs
- Your execution speed
- Exchange fees and liquidity

### Factors Affecting Profitability

1. **Market Volatility**
   - Higher volatility = more opportunities
   - But also higher risk

2. **Trading Volume**
   - Higher volume = better liquidity
   - Easier to execute large orders

3. **Competition**
   - More arbitrageurs = smaller spreads
   - Need faster execution

4. **Exchange Fees**
   - Maker/taker fees impact net profit
   - VIP tiers can reduce fees

---

## Maintenance

### Daily Tasks
- Check bot is running
- Review executed trades
- Monitor balances on exchanges
- Check for errors in logs

### Weekly Tasks
- Review performance metrics
- Adjust parameters if needed
- Rebalance funds between exchanges
- Update strategy if needed

### Monthly Tasks
- Comprehensive performance analysis
- Review and update risk parameters
- Check for Hummingbot updates
- Rotate API keys (recommended)

---

## Support and Resources

### Official Resources
- [Hummingbot Documentation](https://docs.hummingbot.org)
- [Hummingbot Discord](https://discord.gg/hummingbot)
- [Hummingbot GitHub](https://github.com/hummingbot/hummingbot)
- [Hummingbot YouTube](https://youtube.com/@hummingbot)

### Community
- Discord #support channel for help
- Discord #strategies for strategy discussions
- GitHub issues for bug reports
- Reddit r/hummingbot

### Learning
- [Botcamp](https://www.botcamp.xyz) - Official training program
- Hummingbot Academy blog posts
- Community-shared strategies on Discord

---

## Disclaimer

**Important:** This strategy involves financial risk. 

- Past performance doesn't guarantee future results
- Only trade with capital you can afford to lose
- Arbitrage profits can be inconsistent
- Exchange and technical risks exist
- This is not financial advice
- Do your own research (DYOR)

**Start small, test thoroughly, and scale gradually based on proven results.**

---

## Appendix: Strategy Variants

### 1. Multi-Exchange Scanner

Monitor all available exchanges simultaneously:

```python
exchange_pairs = [
    ("kucoin", "kraken"),
    ("kucoin", "bybit"),
    ("kucoin", "mexc"),
    ("kraken", "bybit"),
    ("kraken", "mexc"),
    ("bybit", "mexc"),
]
```

### 2. Volume-Weighted Strategy

Adjust order sizes based on exchange volumes:

```python
def get_order_amount(self, exchange1, exchange2):
    """Adjust order amount based on 24h volume"""
    base_amount = self.order_amount
    
    # Get 24h volumes (implement based on exchange API)
    vol1 = self.get_24h_volume(exchange1)
    vol2 = self.get_24h_volume(exchange2)
    
    # Scale down for low volume exchanges
    min_volume = min(vol1, vol2)
    if min_volume < 1000000:  # $1M threshold
        return base_amount * Decimal("0.5")
    
    return base_amount
```

### 3. Time-Based Strategy

Only trade during high-volume periods:

```python
def should_trade_now(self):
    """Only trade during active hours"""
    import datetime
    
    now = datetime.datetime.now()
    hour = now.hour
    
    # Trade during Asian and European market hours
    if 0 <= hour <= 8 or 13 <= hour <= 20:
        return True
    return False
```

---

## Changelog

- **v1.0** (2025-01-08): Initial release
  - CEX-CEX arbitrage for Kaspa
  - V2 Strategy framework
  - Multi-exchange support

---

**Good luck with your Kaspa arbitrage strategy! Remember to start small and test thoroughly.**
