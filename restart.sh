#!/bin/sh

# Find the process ID (PID) of the price_monitor.py script
PID=$(ps aux | grep 'price_monitor.py' | grep -v 'grep' | awk '{print $2}')

# Check if the PID is found
if [ -z "$PID" ]; then
  echo "price_monitor.py is not running."
else
  # Kill the process
  kill $PID
  echo "Stopped price_monitor.py (PID: $PID)."
fi

# Navigate to the directory containing the price_monitor.py script
cd c:/Users/Deniz/OneDrive/Dokumente/VSC/Python/hypixel-price-monitor

# Start the price_monitor.py script
nohup python price_monitor.py > price_monitor.log 2>&1 &
echo "Restarted price_monitor.py"