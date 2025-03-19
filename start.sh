#!/bin/sh

# Navigate to the directory containing the price_monitor.py script
cd c:/Users/Deniz/OneDrive/Dokumente/VSC/Python/hypixel-price-monitor

# Start the price_monitor.py script
nohup python price_monitor.py > price_monitor.log 2>&1 &
echo "Started price_monitor.py"