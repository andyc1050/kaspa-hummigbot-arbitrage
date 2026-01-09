# Utility Scripts

This folder contains utility scripts to help you manage and monitor your Kaspa arbitrage bots.

## 📜 Available Scripts

### 1. `check_status.sh` - Bot Status Checker

Monitor the status of all your running Hummingbot instances.

**Features:**
- ✅ Check running screen/tmux sessions
- ✅ Check Docker containers status
- ✅ Monitor system resources (CPU, RAM, Disk)
- ✅ View recent errors from logs
- ✅ Count arbitrage opportunities

**Usage:**
```bash
# Make executable (first time only)
chmod +x scripts/check_status.sh

# Run the status check
./scripts/check_status.sh
```

**Example Output:**
```
======================================
  Kaspa Arbitrage Status Check
======================================

Checking Screen Sessions:
  ✓ kas-kucoin-kraken - Running
  ✓ kas-kucoin-bybit - Running
  ✗ kas-mexc-gate - Not found

System Resources:
  CPU Usage: 15.3%
  Memory Usage: 42.8%
  Disk Usage: 35%

Recent errors (last 24h): 0
```

---

### 2. `monitor_performance.py` - Performance Analyzer

Analyze your trading performance from Hummingbot logs.

**Features:**
- 📊 Track arbitrage opportunities
- 💰 Calculate total and average profits
- 📈 Success rate analysis
- 🎯 Daily/monthly profit projections
- 📄 Export to CSV

**Usage:**
```bash
# Analyze last 24 hours
python scripts/monitor_performance.py

# Analyze last 7 days
python scripts/monitor_performance.py --days 7

# Specify custom log path
python scripts/monitor_performance.py --log-path /path/to/logs

# Export results to CSV
python scripts/monitor_performance.py --days 7 --export report.csv
```

**Example Output:**
```
🤖 KASPA ARBITRAGE PERFORMANCE REPORT
====================================

📅 Period: Last 7 day(s)

📊 TRADING ACTIVITY
  Opportunities Detected:          145
  Trades Executed:                  87
  Trades Completed:                 78
  Trades Failed:                     9

💰 PROFITABILITY
  Total Profit:                 $127.50
  Average Profit/Trade:           $1.63
  Average Opportunity %:          0.58%

📈 PERFORMANCE METRICS
  Success Rate:                   89.7%
  Trades Per Day:                 11.1

🎯 PROJECTIONS
  Estimated Daily Profit:        $18.21
  Estimated Monthly Profit:     $546.30
```

---

## 🚀 Quick Start

### Installation

1. **Download the scripts** to your repository
2. **Make them executable** (Linux/Mac):
   ```bash
   chmod +x scripts/check_status.sh
   chmod +x scripts/monitor_performance.py
   ```

3. **Install dependencies** (for Python script):
   ```bash
   # Python 3 is required (usually pre-installed)
   python3 --version
   ```

### Setting Up

Both scripts will automatically try to find your Hummingbot logs in:
- `~/hummingbot_files/logs/`
- `~/hummingbot/logs/`
- `./logs/`

If your logs are elsewhere, specify the path:
```bash
# For check_status.sh - edit the script and update log_dirs array

# For monitor_performance.py
python scripts/monitor_performance.py --log-path /custom/path/logs
```

---

## 📋 Use Cases

### Daily Monitoring Routine

```bash
# Morning check
./scripts/check_status.sh

# View yesterday's performance
python scripts/monitor_performance.py --days 1

# Weekly review (every Sunday)
python scripts/monitor_performance.py --days 7 --export weekly_report.csv
```

### Troubleshooting

**Bot not executing trades?**
```bash
# Check if bot is running
./scripts/check_status.sh

# Look for errors in performance
python scripts/monitor_performance.py --days 1
```

**Low success rate?**
```bash
# Analyze last 3 days
python scripts/monitor_performance.py --days 3

# Check the assessment section for recommendations
```

### Performance Tracking

Create a cron job to automatically generate daily reports:

```bash
# Add to crontab (crontab -e)
0 0 * * * cd /path/to/repo && python scripts/monitor_performance.py --days 1 --export daily_$(date +\%Y\%m\%d).csv
```

---

## 🔧 Customization

### Modifying `check_status.sh`

**Add more screen sessions:**
```bash
# Edit the sessions array (line ~36)
sessions=(
    "kas-kucoin-kraken"
    "kas-kucoin-bybit"
    "kas-mexc-gate"
    "kas-your-new-pair"  # Add your own
)
```

**Add more Docker containers:**
```bash
# Edit the containers array (line ~58)
containers=(
    "hummingbot-kas-kucoin-kraken"
    "hummingbot-kas-your-container"  # Add your own
)
```

### Modifying `monitor_performance.py`

**Change date range default:**
```python
# Line ~17
parser.add_argument('--days', type=int, default=7)  # Change from 1 to 7
```

**Add custom metrics:**
```python
# Add in calculate_metrics() method
metrics['your_metric'] = your_calculation
```

---

## 🐛 Troubleshooting

### `check_status.sh` Issues

**Error: "Permission denied"**
```bash
chmod +x scripts/check_status.sh
```

**Error: "screen: command not found"**
```bash
# Install screen
sudo apt-get install screen  # Ubuntu/Debian
brew install screen          # macOS
```

**No logs found:**
- Check if Hummingbot is actually running
- Verify log path in the script matches your setup
- Ensure logs directory exists

### `monitor_performance.py` Issues

**Error: "No module named..."**
```bash
# All required modules are in Python standard library
# Ensure you're using Python 3:
python3 scripts/monitor_performance.py
```

**No data in report:**
- Check if log file exists: `logs/hummingbot_logs.log`
- Verify you have trading activity in the time period
- Try increasing `--days` parameter

**Incorrect profit calculations:**
- Log format may have changed
- Check Hummingbot version compatibility
- Open an issue on GitHub

---

## 📊 Understanding the Metrics

### Success Rate
```
Success Rate = (Completed Trades / Executed Trades) × 100
```
- **>70%**: Excellent - strategy working well
- **50-70%**: Good - minor optimization possible
- **<50%**: Poor - review parameters

### Execution Rate
```
Execution Rate = (Executed Trades / Opportunities) × 100
```
- Low rate means `min_profitability` might be too high
- High rate is good - capturing opportunities

### Average Profit
Total profit divided by completed trades. Should exceed:
- Exchange fees (typically 0.2% × 2 = 0.4%)
- Plus your target profit (0.3-0.5%)

---

## 🆘 Getting Help

If these scripts don't work:

1. **Check Hummingbot logs manually:**
   ```bash
   tail -f ~/hummingbot/logs/hummingbot_logs.log
   ```

2. **Verify your setup:**
   - Is Hummingbot running?
   - Are logs being generated?
   - What version of Hummingbot are you using?

3. **Open an issue** on GitHub with:
   - Error message
   - Your Hummingbot version
   - Operating system
   - Log excerpt (remove API keys!)

---

## 🔄 Updates

**Script Versions:**
- `check_status.sh` - v1.0 (2025-01-09)
- `monitor_performance.py` - v1.0 (2025-01-09)

Check the main repository for updates!

---

## 🤝 Contributing

Found a bug? Want to add a feature?

1. Fork the repository
2. Modify the scripts
3. Test thoroughly
4. Submit a pull request

**Ideas for contributions:**
- Real-time monitoring dashboard
- Telegram/Discord notifications
- More detailed trade analysis
- Multi-bot comparison
- Database storage for historical data

---

## 📄 License

These scripts are part of the Kaspa Arbitrage Bot repository and are licensed under MIT License.

---

**Happy monitoring! 📊🚀**
