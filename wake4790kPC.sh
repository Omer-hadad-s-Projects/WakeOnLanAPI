MAC_ADDRESS="40:8D:5C:42:20:7A"
TARGET_IP="192.168.0.14"
FRIENDLY_NAME=4790k-PC

wakeonlan "$MAC_ADDRESS"
echo "WOL packet sent to $FRIENDLY_NAME"
