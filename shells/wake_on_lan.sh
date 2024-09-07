#!/usr/bin/env bash

MAC_ADDRESS="$1"
TARGET_IP="$2"
TIMEOUT="$3"

PING_RETRIES=5

wakeonlan "$MAC_ADDRESS"
echo "WOL packet sent to $TARGET_IP"

CURRENT_TIMESTAMP=$(date +%s)
START_TIMESTAMP=$CURRENT_TIMESTAMP
while true; do
    if ping -c $PING_RETRIES $TARGET_IP >/dev/null 2>&1; then
        echo "$TARGET_IP is now online!"
        exit 0
    else
        echo "$TARGET_IP is still offline"
    fi
    CURRENT_TIMESTAMP=$(date +%s)
    TIME_PASSED=$(($CURRENT_TIMESTAMP - $START_TIMESTAMP))
    echo "Time passed: $TIME_PASSED seconds"
    if [ $TIME_PASSED -ge $TIMEOUT ]; then
        echo "Timeout reached. $TARGET_IP is still offline."
        exit 1
    fi
done
