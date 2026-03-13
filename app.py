from flask import Flask, request, jsonify
from wakeonlan import send_magic_packet
from datetime import datetime, timezone
import subprocess
import time
import os

app = Flask(__name__)
TIMEOUT = 30
PING_RETRIES = 5
PORT = os.getenv('APP_PORT', 5000)


def is_device_online(ip_address):
    """Check if a device is reachable via ping."""
    try:
        result = subprocess.run(
            ['ping', '-c', str(PING_RETRIES), ip_address],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the API is running."""
    return jsonify({
        "status": "healthy",
        "service": "WakeOnLanAPI",
        "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    }), 200

@app.route('/wake', methods=['POST'])
def wake_device():
    """Send WOL packet and wait for device to come online."""
    data = request.get_json()
    mac_address = data.get('mac_address')
    ip_address = data.get('ip_address')

    if not mac_address or not ip_address:
        return jsonify({"error": "Both mac_address and ip_address are required."}), 400

    start_time = time.time()

    try:
        send_magic_packet(mac_address)

        while time.time() - start_time < TIMEOUT:
            if is_device_online(ip_address):
                elapsed = int(time.time() - start_time)
                return jsonify({
                    "result": "success",
                    "duration_seconds": elapsed
                }), 200

            time.sleep(1)

        return jsonify({
            "result": "timeout",
            "duration_seconds": TIMEOUT
        }), 504

    except Exception as e:
        elapsed = int(time.time() - start_time)
        return jsonify({
            "result": "error",
            "duration_seconds": elapsed,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
