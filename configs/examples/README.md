# Configuration Examples

This folder contains example configuration files for the Kaspa arbitrage strategy using Hummingbot's built-in AMM Arbitrage strategy.

## 📁 Available Examples

| File | Exchange Pair | Liquidity | Recommended For |
|------|--------------|-----------|-----------------|
| `config_kucoin_kraken.yml` | KuCoin ↔ Kraken | High | Beginners, larger orders |
| `config_kucoin_bybit.yml` | KuCoin ↔ Bybit | High | All users |
| `config_mexc_gate.yml` | MEXC ↔ Gate.io | Medium | Advanced users |

## 🚀 How to Use

### Step 1: Copy Example File

```bash
# Copy an example to your Hummingbot conf directory
cp configs/examples/config_kucoin_kraken.yml ~/hummingbot/conf/my_kas_arbitrage.yml
```

### Step 2: Customize Parameters

Edit the copied file to match your preferences:

```yaml
order_amount: 100.0              # Your order size
min_profitability: 0.005         # Your profit threshold
market_1_slippage_buffer: 0.001  # Adjust for exchange liquidity
```

### Step 3: Import in Hummingbot

```bash
# In Hummingbot terminal
import my_kas_arbitrage.yml

# Verify configuration
config

# Start trading
start
```

## 📊 Parameter Guidelines

### order_amount

The amount of KAS to trade per arbitrage opportunity.

| Experience Level | Recommended Amount | USD Value (@ $0.05/KAS) |
|-----------------|-------------------|------------------------|
| Testing | 50-100 KAS | $2.50-$5.00 |
| Beginner | 100-200 KAS | $5.00-$10.00 |
| Intermediate | 200-500 KAS | $10.00-$25.00 |
| Advanced | 500-2000 KAS | $25.00-$100.00 |

**Tips:**
- Start small and scale gradually
- Consider exchange liquidity
- Ensure sufficient balance on both exchanges

### min_profitability

Minimum profit percentage required to execute trade (after fees).

| Value | Description | Trade Frequency | Risk Level |
|-------|-------------|----------------|------------|
| 0.003 (0.3%) | Aggressive | High | Higher |
| 0.005 (0.5%) | Moderate | Medium | Moderate |
| 0.008 (0.8%) | Conservative | Lower | Lower |

**Considerations:**
- Lower threshold = more trades but lower profit/trade
- Higher threshold = fewer trades but higher profit/trade
- Factor in exchange fees (typically 0.1% per side)
- Account for slippage and price volatility

### slippage_buffer

Price adjustment to account for market movement during execution.

| Exchange Tier | Liquidity | Recommended Buffer |
|--------------|-----------|-------------------|
| Tier 1 (Binance, KuCoin, Kraken) | High | 0.001 (0.1%) |
| Tier 2 (Bybit, Gate.io) | Good | 0.001-0.0012 (0.1-0.12%) |
| Tier 3 (MEXC, others) | Medium | 0.0015 (0.15%) |

**Adjust based on:**
- 24-hour trading volume
- Order book depth
- Historical price volatility
- Your order size relative to market

### concurrent_orders_submission

Whether to submit buy and sell orders simultaneously.

| Setting | Execution | Risk | Recommended When |
|---------|-----------|------|------------------|
| `true` | Faster | Higher | High liquidity, stable prices |
| `false` | Slower | Lower | Low liquidity, volatile prices |

**Pros of concurrent (true):**
- Faster execution
- Captures opportunities before they disappear
- Better for high-frequency strategies

**Cons of concurrent (true):**
- Risk of partial fills (one side executes, other doesn't)
- Higher execution risk in volatile markets
- May require manual intervention if one order fails

## 🔧 Advanced Configuration

### Optional Parameters

You can add these parameters to any configuration file:

```yaml
# Maximum time to wait before cancelling unfilled orders (seconds)
order_refresh_time: 30.0

# Only simulate trades without executing (testing)
debug_mode: false

# Use external price feeds for more accurate pricing
use_rate_oracle: false

# Override default trading fees
taker_fee: 0.001  # 0.1%
maker_fee: 0.0005 # 0.05%

# Minimum order size (exchange specific)
min_order_size: 10.0
```

## 🎯 Choosing the Right Exchange Pair

### High Liquidity Pairs (Best for Beginners)

**KuCoin ↔ Kraken**
- ✅ Both have high KAS volume
- ✅ Reliable API
- ✅ Lower slippage
- ✅ Good for larger orders

**KuCoin ↔ Bybit**
- ✅ High liquidity on both
- ✅ Fast execution
- ✅ Good API stability

### Medium Liquidity Pairs (For Experienced Users)

**MEXC ↔ Gate.io**
- ⚠️ Medium liquidity
- ⚠️ May have larger spreads
- ✅ Potentially more opportunities
- ⚠️ Requires careful parameter tuning

## ⚠️ Important Security Notes

### DO NOT Commit API Keys!

**NEVER** include real API keys in configuration files that you commit to Git/GitHub!

```yaml
# ❌ WRONG - Don't do this!
api_key: "your_actual_api_key_here"
api_secret: "your_actual_secret_here"

# ✅ CORRECT - Hummingbot prompts for these
# No API keys in config file!
```

### Protecting Your Configuration

1. **Use .gitignore**
   ```
   conf/*.yml
   !conf/examples/*.yml
   ```

2. **Store credentials separately**
   - Hummingbot encrypts and stores credentials securely
   - Never share your `conf/` directory

3. **Review before committing**
   ```bash
   git diff  # Check what you're about to commit
   ```

## 📋 Pre-Flight Checklist

Before starting your bot:

- [ ] Copied and customized configuration file
- [ ] Verified API keys are set up (via `connect` command)
- [ ] Checked balances on both exchanges (`balance` command)
- [ ] Reviewed and adjusted parameters
- [ ] Tested with paper trading mode first (`paper_trading`)
- [ ] Set up monitoring (check `logs/` directory)
- [ ] Prepared to monitor first few trades closely

## 🔍 Testing Your Configuration

### Paper Trading Mode

```bash
# In Hummingbot
paper_trading

# Import your config
import my_kas_arbitrage.yml

# Start (no real money!)
start

# Monitor for issues
status
```

### Small Capital Test

After paper trading:

1. Start with minimal capital ($50-100)
2. Run for 24-48 hours
3. Monitor closely
4. Review performance
5. Scale up if profitable

## 📈 Monitoring and Optimization

### Check Strategy Status

```bash
# Real-time status
status

# Recent trade history
history

# Performance metrics
performance

# Balance check
balance
```

### Log Analysis

```bash
# View live logs
tail -f logs/hummingbot_logs.log

# Search for arbitrage events
grep "arbitrage" logs/hummingbot_logs.log

# Check for errors
grep "ERROR" logs/hummingbot_logs.log
```

### Optimization Tips

1. **Track key metrics:**
   - Win rate (% profitable trades)
   - Average profit per trade
   - Total daily profit
   - Failed trade reasons

2. **Adjust parameters based on results:**
   - Too many failed trades? Increase slippage_buffer
   - Too few opportunities? Lower min_profitability
   - Orders not filling? Reduce order_amount

3. **Rebalance regularly:**
   - Monitor exchange balances
   - Transfer funds as needed
   - Maintain ~50/50 USDT/KAS split

## 🆘 Troubleshooting

### Common Issues

**"Trading pair not found"**
- Verify KAS-USDT is available on both exchanges
- Check correct pair format (some use `/` instead of `-`)

**"Insufficient balance"**
- Check you have USDT on buying exchange
- Check you have KAS on selling exchange
- Ensure amounts account for fees

**"No arbitrage opportunities found"**
- Lower `min_profitability` threshold
- Add more exchange pairs
- Check if trading is halted on exchanges

**"Orders not filling"**
- Increase `market_X_slippage_buffer`
- Reduce `order_amount`
- Check exchange order book depth

**"API rate limit exceeded"**
- Reduce polling frequency
- Check if using multiple bots on same API key
- Consider upgrading to higher API tier

## 📚 Additional Resources

- [Main Setup Guide](../../docs/KASPA_ARBITRAGE_SETUP_GUIDE.md)
- [Simple Strategy Guide](../../docs/KASPA_SIMPLE_STRATEGY_GUIDE.md)
- [Hummingbot AMM Arb Docs](https://docs.hummingbot.org/strategies/amm-arb/)
- [Hummingbot Discord](https://discord.gg/hummingbot)

## 🤝 Contributing

Found a good configuration that works well? Consider sharing it!

1. Test thoroughly with real trades
2. Document your results and parameters
3. Submit a pull request with your example config
4. Help others in the community!

---

**Happy arbitraging! 🚀**

Remember: Start small, test thoroughly, and scale gradually!
