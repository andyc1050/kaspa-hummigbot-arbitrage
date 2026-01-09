# Contributing to Kaspa Arbitrage Bot

First off, thank you for considering contributing to this project! 🎉

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Screenshots** if applicable
- **Environment details** (OS, Hummingbot version, Python version)
- **Configuration** (remove API keys!)
- **Log excerpts** showing the error

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

- **Clear use case** - what problem does it solve?
- **Detailed description** of the proposed feature
- **Examples** of how it would work
- **Mockups or diagrams** if applicable

### Code Contributions

#### Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/kaspa-hummingbot-arbitrage.git
   cd kaspa-hummingbot-arbitrage
   ```

3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

#### Development Guidelines

**Code Style:**
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Comment complex logic

**Example:**
```python
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
    # Implementation here
```

**Testing:**
- Test your changes thoroughly
- Use paper trading mode first
- Test with small amounts before larger trades
- Verify on multiple exchange pairs if applicable

**Documentation:**
- Update relevant documentation files
- Add comments for complex logic
- Update README.md if needed
- Include usage examples

#### Pull Request Process

1. **Update documentation** as needed
2. **Test thoroughly** with paper trading
3. **Commit with clear messages**
   ```bash
   git commit -m "Add feature: multi-threaded opportunity detection"
   # or
   git commit -m "Fix: balance check not accounting for locked funds"
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Provide clear title and description
   - Reference related issues
   - Explain what changed and why
   - Include test results

6. **Respond to feedback**
   - Be open to suggestions
   - Make requested changes
   - Update your PR as needed

#### Commit Message Guidelines

Good commit messages:
```
Add support for Binance futures trading
Fix incorrect profit calculation for high-fee exchanges
Update documentation for Docker installation
Improve error handling in order execution
```

Bad commit messages:
```
update
fixed stuff
changes
wip
```

### Documentation Contributions

Documentation improvements are highly valued!

- Fix typos and grammar
- Clarify confusing sections
- Add examples and use cases
- Improve formatting
- Translate to other languages

### Community

- Be respectful and constructive
- Help others in discussions
- Share your trading experiences (no financial advice!)
- Suggest improvements

## Development Setup

### Prerequisites

- Python 3.10+
- Hummingbot development environment
- Git

### Local Development

```bash
# Clone the repo
git clone https://github.com/YOUR-USERNAME/kaspa-hummingbot-arbitrage.git
cd kaspa-hummingbot-arbitrage

# Set up Hummingbot (if not already done)
git clone https://github.com/hummingbot/hummingbot.git
cd hummingbot
./install
conda activate hummingbot

# Copy strategy to Hummingbot
cp ../kaspa-hummingbot-arbitrage/kaspa_arbitrage_v2.py scripts/

# Test your changes
./start
```

### Testing Your Strategy

1. **Paper Trading First**
   ```bash
   # In Hummingbot
   paper_trading
   import kaspa_arbitrage_v2
   start
   ```

2. **Small Capital Test**
   - Use real exchanges but tiny amounts ($10-50)
   - Monitor closely for 24-48 hours
   - Check logs for errors

3. **Full Testing**
   - Gradually increase capital
   - Test edge cases
   - Verify error handling

## Code of Conduct

### Our Standards

**Positive behavior:**
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards others

**Unacceptable behavior:**
- Harassment of any kind
- Publishing others' private information
- Trolling or insulting comments
- Other unprofessional conduct

### Enforcement

Instances of unacceptable behavior may result in:
- Warning
- Temporary ban
- Permanent ban

Report issues to [your contact method].

## Questions?

- Open an issue for discussion
- Join Hummingbot Discord #strategies channel
- Check existing documentation

## Attribution

This project follows the [Hummingbot contribution guidelines](https://github.com/hummingbot/hummingbot/blob/master/CONTRIBUTING.md) where applicable.

---

**Thank you for contributing!** 🚀

Every contribution, no matter how small, helps make this project better for everyone.
