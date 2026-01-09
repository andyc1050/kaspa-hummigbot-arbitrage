#!/usr/bin/env python3
"""
Kaspa Arbitrage Performance Monitor

This script analyzes Hummingbot log files to track arbitrage performance,
calculate profits, and generate performance reports.

Usage:
    python monitor_performance.py
    python monitor_performance.py --log-path /path/to/logs
    python monitor_performance.py --days 7
"""

import argparse
import os
import re
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path


class KaspaArbitrageMonitor:
    """Monitor and analyze Kaspa arbitrage trading performance"""
    
    def __init__(self, log_path=None, days=1):
        """
        Initialize the monitor
        
        Args:
            log_path: Path to Hummingbot logs directory
            days: Number of days to analyze (default: 1)
        """
        self.days = days
        self.log_path = log_path or self.find_log_path()
        self.trades = []
        self.stats = defaultdict(int)
        
    def find_log_path(self):
        """Find Hummingbot log directory"""
        possible_paths = [
            Path.home() / "hummingbot_files" / "logs",
            Path.home() / "hummingbot" / "logs",
            Path("logs"),
            Path(".") / "logs",
        ]
        
        for path in possible_paths:
            if path.exists() and path.is_dir():
                return path
        
        raise FileNotFoundError("Could not find Hummingbot logs directory")
    
    def parse_log_file(self):
        """Parse Hummingbot log file for arbitrage trades"""
        log_file = self.log_path / "hummingbot_logs.log"
        
        if not log_file.exists():
            print(f"❌ Log file not found: {log_file}")
            return
        
        print(f"📊 Analyzing logs from: {log_file}")
        print(f"📅 Looking back {self.days} day(s)")
        print("")
        
        cutoff_date = datetime.now() - timedelta(days=self.days)
        
        # Patterns to match in logs
        patterns = {
            'opportunity': re.compile(r'arbitrage opportunity.*?profit.*?(\d+\.?\d*)%', re.IGNORECASE),
            'executed': re.compile(r'arbitrage.*?executed', re.IGNORECASE),
            'completed': re.compile(r'arbitrage.*?complete.*?profit.*?(\$?\d+\.?\d*)', re.IGNORECASE),
            'failed': re.compile(r'arbitrage.*?fail', re.IGNORECASE),
            'error': re.compile(r'ERROR.*arbitrage', re.IGNORECASE),
            'order_filled': re.compile(r'order filled.*?(\d+\.?\d*)\s*(KAS|USDT)', re.IGNORECASE),
        }
        
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                try:
                    # Extract timestamp
                    timestamp_match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                    if not timestamp_match:
                        continue
                    
                    timestamp_str = timestamp_match.group(1)
                    log_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                    
                    # Skip if outside date range
                    if log_time < cutoff_date:
                        continue
                    
                    # Check for different event types
                    if patterns['opportunity'].search(line):
                        self.stats['opportunities'] += 1
                        profit_match = patterns['opportunity'].search(line)
                        if profit_match:
                            profit = float(profit_match.group(1))
                            self.stats['total_opportunity_profit'] += profit
                    
                    if patterns['executed'].search(line):
                        self.stats['executed'] += 1
                    
                    if patterns['completed'].search(line):
                        self.stats['completed'] += 1
                        profit_match = patterns['completed'].search(line)
                        if profit_match:
                            profit_str = profit_match.group(1).replace('$', '')
                            profit = float(profit_str)
                            self.stats['total_profit'] += profit
                    
                    if patterns['failed'].search(line):
                        self.stats['failed'] += 1
                    
                    if patterns['error'].search(line):
                        self.stats['errors'] += 1
                
                except Exception as e:
                    # Skip problematic lines
                    continue
    
    def calculate_metrics(self):
        """Calculate performance metrics"""
        metrics = {}
        
        # Success rate
        total_attempts = self.stats['executed']
        if total_attempts > 0:
            metrics['success_rate'] = (self.stats['completed'] / total_attempts) * 100
        else:
            metrics['success_rate'] = 0
        
        # Average profit per trade
        if self.stats['completed'] > 0:
            metrics['avg_profit'] = self.stats['total_profit'] / self.stats['completed']
        else:
            metrics['avg_profit'] = 0
        
        # Average opportunity profit
        if self.stats['opportunities'] > 0:
            metrics['avg_opp_profit'] = self.stats['total_opportunity_profit'] / self.stats['opportunities']
        else:
            metrics['avg_opp_profit'] = 0
        
        # Trades per day
        metrics['trades_per_day'] = self.stats['completed'] / max(self.days, 1)
        
        # Estimated daily profit
        metrics['daily_profit'] = metrics['trades_per_day'] * metrics['avg_profit']
        
        # Estimated monthly profit (30 days)
        metrics['monthly_profit'] = metrics['daily_profit'] * 30
        
        return metrics
    
    def print_report(self):
        """Print performance report"""
        metrics = self.calculate_metrics()
        
        print("=" * 60)
        print("🤖 KASPA ARBITRAGE PERFORMANCE REPORT")
        print("=" * 60)
        print()
        
        print(f"📅 Period: Last {self.days} day(s)")
        print(f"📁 Log Path: {self.log_path}")
        print()
        
        print("-" * 60)
        print("📊 TRADING ACTIVITY")
        print("-" * 60)
        print(f"  Opportunities Detected:     {self.stats['opportunities']:>8}")
        print(f"  Trades Executed:            {self.stats['executed']:>8}")
        print(f"  Trades Completed:           {self.stats['completed']:>8}")
        print(f"  Trades Failed:              {self.stats['failed']:>8}")
        print(f"  Errors Encountered:         {self.stats['errors']:>8}")
        print()
        
        print("-" * 60)
        print("💰 PROFITABILITY")
        print("-" * 60)
        print(f"  Total Profit:               ${self.stats['total_profit']:>8.2f}")
        print(f"  Average Profit/Trade:       ${metrics['avg_profit']:>8.2f}")
        print(f"  Average Opportunity %:      {metrics['avg_opp_profit']:>7.2f}%")
        print()
        
        print("-" * 60)
        print("📈 PERFORMANCE METRICS")
        print("-" * 60)
        print(f"  Success Rate:               {metrics['success_rate']:>7.1f}%")
        print(f"  Trades Per Day:             {metrics['trades_per_day']:>8.1f}")
        print()
        
        print("-" * 60)
        print("🎯 PROJECTIONS")
        print("-" * 60)
        print(f"  Estimated Daily Profit:     ${metrics['daily_profit']:>8.2f}")
        print(f"  Estimated Monthly Profit:   ${metrics['monthly_profit']:>8.2f}")
        print()
        
        # Performance assessment
        print("-" * 60)
        print("💡 ASSESSMENT")
        print("-" * 60)
        
        if metrics['success_rate'] >= 70:
            print("  ✅ Excellent success rate!")
        elif metrics['success_rate'] >= 50:
            print("  ⚠️  Moderate success rate - consider optimization")
        else:
            print("  ❌ Low success rate - review strategy parameters")
        
        if self.stats['errors'] > self.stats['completed'] * 0.1:
            print("  ⚠️  High error rate - check logs for issues")
        
        if self.stats['opportunities'] > 0:
            execution_rate = (self.stats['executed'] / self.stats['opportunities']) * 100
            if execution_rate < 50:
                print(f"  ⚠️  Low execution rate ({execution_rate:.1f}%) - check min_profitability")
        
        print()
        print("=" * 60)
        print()
    
    def export_csv(self, filename="performance_report.csv"):
        """Export performance data to CSV"""
        metrics = self.calculate_metrics()
        
        with open(filename, 'w') as f:
            f.write("Metric,Value\n")
            f.write(f"Period (days),{self.days}\n")
            f.write(f"Opportunities,{self.stats['opportunities']}\n")
            f.write(f"Executed,{self.stats['executed']}\n")
            f.write(f"Completed,{self.stats['completed']}\n")
            f.write(f"Failed,{self.stats['failed']}\n")
            f.write(f"Errors,{self.stats['errors']}\n")
            f.write(f"Total Profit,{self.stats['total_profit']:.2f}\n")
            f.write(f"Average Profit,{metrics['avg_profit']:.2f}\n")
            f.write(f"Success Rate,{metrics['success_rate']:.1f}\n")
            f.write(f"Trades Per Day,{metrics['trades_per_day']:.1f}\n")
            f.write(f"Daily Profit,{metrics['daily_profit']:.2f}\n")
            f.write(f"Monthly Profit,{metrics['monthly_profit']:.2f}\n")
        
        print(f"📄 Report exported to: {filename}")
        print()


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Monitor Kaspa arbitrage performance from Hummingbot logs'
    )
    parser.add_argument(
        '--log-path',
        type=str,
        help='Path to Hummingbot logs directory'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=1,
        help='Number of days to analyze (default: 1)'
    )
    parser.add_argument(
        '--export',
        type=str,
        help='Export results to CSV file'
    )
    
    args = parser.parse_args()
    
    try:
        # Create monitor
        monitor = KaspaArbitrageMonitor(
            log_path=Path(args.log_path) if args.log_path else None,
            days=args.days
        )
        
        # Parse logs
        monitor.parse_log_file()
        
        # Print report
        monitor.print_report()
        
        # Export if requested
        if args.export:
            monitor.export_csv(args.export)
    
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print()
        print("Please specify the log path:")
        print("  python monitor_performance.py --log-path /path/to/logs")
        return 1
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
