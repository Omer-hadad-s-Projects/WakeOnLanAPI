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

    logs = []

    try:
        send_magic_packet(mac_address)
        logs.append(f"WOL packet sent to {mac_address} (target: {ip_address})")

        start_time = time.time()

        while time.time() - start_time < TIMEOUT:
            if is_device_online(ip_address):
                elapsed = int(time.time() - start_time)
                logs.append(f"{ip_address} is now online!")
                logs.append(f"Time taken: {elapsed} seconds")
                return jsonify({"output": logs, "exit_code": 0, "online": True}), 200

            elapsed = int(time.time() - start_time)
            logs.append(f"{ip_address} is still offline (elapsed: {elapsed}s)")
            time.sleep(1)

        # Timeout reached
        logs.append(
            f"Timeout reached after {TIMEOUT} seconds. {ip_address} is still offline.")
        return jsonify({"output": logs, "exit_code": 1, "online": False}), 200

    except Exception as e:
        logs.append(f"Error: {str(e)}")
        return jsonify({"error": str(e), "output": logs}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
