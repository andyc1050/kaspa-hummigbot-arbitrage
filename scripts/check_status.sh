#!/bin/bash

###############################################################################
# Kaspa Arbitrage Status Checker
# 
# This script checks the status of multiple Hummingbot instances running
# Kaspa arbitrage strategies.
#
# Usage: ./check_status.sh
###############################################################################

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}  Kaspa Arbitrage Status Check${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Function to check if screen session exists
check_screen_session() {
    local session_name=$1
    if screen -list | grep -q "$session_name"; then
        return 0
    else
        return 1
    fi
}

# Function to check Docker container
check_docker_container() {
    local container_name=$1
    if docker ps --format '{{.Names}}' | grep -q "^${container_name}$"; then
        return 0
    else
        return 1
    fi
}

# Check Screen Sessions (if using screen/tmux)
echo -e "${YELLOW}Checking Screen Sessions:${NC}"
echo ""

sessions=(
    "kas-kucoin-kraken"
    "kas-kucoin-bybit"
    "kas-mexc-gate"
)

for session in "${sessions[@]}"; do
    if check_screen_session "$session"; then
        echo -e "  ${GREEN}✓${NC} $session - Running"
    else
        echo -e "  ${RED}✗${NC} $session - Not found"
    fi
done

echo ""

# Check Docker Containers (if using Docker)
echo -e "${YELLOW}Checking Docker Containers:${NC}"
echo ""

containers=(
    "hummingbot-kas-kucoin-kraken"
    "hummingbot-kas-kucoin-bybit"
    "hummingbot-kas-mexc-gate"
)

for container in "${containers[@]}"; do
    if check_docker_container "$container"; then
        echo -e "  ${GREEN}✓${NC} $container - Running"
    else
        echo -e "  ${RED}✗${NC} $container - Not running"
    fi
done

echo ""

# Show active Hummingbot processes
echo -e "${YELLOW}Active Hummingbot Processes:${NC}"
echo ""

if pgrep -f "hummingbot" > /dev/null; then
    ps aux | grep -i hummingbot | grep -v grep | awk '{print "  PID: "$2" | User: "$1" | CPU: "$3"% | Mem: "$4"%"}'
else
    echo -e "  ${RED}No Hummingbot processes found${NC}"
fi

echo ""

# Check system resources
echo -e "${YELLOW}System Resources:${NC}"
echo ""

# CPU usage
cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
echo -e "  CPU Usage: ${cpu_usage}%"

# Memory usage
mem_usage=$(free | grep Mem | awk '{printf("%.2f", $3/$2 * 100.0)}')
echo -e "  Memory Usage: ${mem_usage}%"

# Disk usage
disk_usage=$(df -h / | awk 'NR==2 {print $5}')
echo -e "  Disk Usage: ${disk_usage}"

echo ""

# Check log files
echo -e "${YELLOW}Recent Errors in Logs:${NC}"
echo ""

log_dirs=(
    "$HOME/hummingbot_files/logs"
    "$HOME/hummingbot/logs"
    "./logs"
)

found_logs=false

for log_dir in "${log_dirs[@]}"; do
    if [ -d "$log_dir" ]; then
        found_logs=true
        log_file="$log_dir/hummingbot_logs.log"
        
        if [ -f "$log_file" ]; then
            error_count=$(grep -c "ERROR" "$log_file" 2>/dev/null || echo "0")
            echo -e "  Log: $log_file"
            echo -e "  Recent errors (last 24h): ${error_count}"
            
            if [ "$error_count" -gt 0 ]; then
                echo -e "  ${RED}Last 3 errors:${NC}"
                grep "ERROR" "$log_file" | tail -n 3 | sed 's/^/    /'
            fi
            echo ""
        fi
    fi
done

if [ "$found_logs" = false ]; then
    echo -e "  ${YELLOW}No log directories found${NC}"
fi

echo ""

# Show recent trades (if available)
echo -e "${YELLOW}Recent Activity:${NC}"
echo ""

if [ -f "$HOME/hummingbot/logs/hummingbot_logs.log" ]; then
    arbitrage_count=$(grep -c "arbitrage" "$HOME/hummingbot/logs/hummingbot_logs.log" 2>/dev/null || echo "0")
    echo -e "  Arbitrage opportunities detected today: ${arbitrage_count}"
elif [ -f "./logs/hummingbot_logs.log" ]; then
    arbitrage_count=$(grep -c "arbitrage" "./logs/hummingbot_logs.log" 2>/dev/null || echo "0")
    echo -e "  Arbitrage opportunities detected today: ${arbitrage_count}"
else
    echo -e "  ${YELLOW}No activity logs found${NC}"
fi

echo ""
echo -e "${BLUE}======================================${NC}"
echo -e "${GREEN}Status check complete!${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Instructions
echo -e "${YELLOW}Quick Commands:${NC}"
echo ""
echo "  Attach to screen session:"
echo "    screen -r kas-kucoin-kraken"
echo ""
echo "  View Docker logs:"
echo "    docker logs hummingbot-kas-kucoin-kraken"
echo ""
echo "  View live logs:"
echo "    tail -f logs/hummingbot_logs.log"
echo ""
