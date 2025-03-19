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