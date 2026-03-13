from flask import Flask, request, jsonify
from wakeonlan import send_magic_packet
from datetime import datetime, timezone
import subprocess
import time
import os

app = Flask(__name__)
DEFAULT_TIMEOUT = 30
MAX_TIMEOUT = 60
PORT = os.getenv('APP_PORT', 5000)


def get_elapsed_seconds(start_time):
    return int(time.time() - start_time)


def get_ping_timeout(max_wait_seconds):
    return max(0.1, min(1, max_wait_seconds))


def is_device_online(ip_address, max_wait_seconds):
    """Check if a device is reachable via ping."""
    try:
        result = subprocess.run(
            ['ping', '-c', '1', ip_address],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=get_ping_timeout(max_wait_seconds)
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def get_wake_request(data):
    mac_address = data.get('mac_address')
    ip_address = data.get('ip_address')
    requested_timeout = data.get('timeout_seconds', DEFAULT_TIMEOUT)

    if not mac_address or not ip_address:
        return None, "Both mac_address and ip_address are required."

    try:
        requested_timeout = int(requested_timeout)
    except (TypeError, ValueError):
        return None, "timeout_seconds must be an integer."

    if requested_timeout <= 0:
        return None, "timeout_seconds must be greater than 0."

    return {
        "mac_address": mac_address,
        "ip_address": ip_address,
        "timeout_seconds": min(requested_timeout, MAX_TIMEOUT)
    }, None


def wait_for_device_online(ip_address, timeout_seconds, start_time):
    deadline = start_time + timeout_seconds

    while True:
        remaining_seconds = deadline - time.time()

        if remaining_seconds <= 0:
            return False

        if is_device_online(ip_address, remaining_seconds):
            return True

        time.sleep(min(1, max(0, deadline - time.time())))


def build_success_response(start_time):
    return jsonify({
        "result": "success",
        "duration_seconds": get_elapsed_seconds(start_time)
    }), 200


def build_timeout_response(timeout_seconds):
    return jsonify({
        "result": "timeout",
        "duration_seconds": timeout_seconds
    }), 503


def build_error_response(start_time, error):
    return jsonify({
        "result": "error",
        "duration_seconds": get_elapsed_seconds(start_time),
        "error": str(error)
    }), 500


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
    wake_request, validation_error = get_wake_request(data)

    if validation_error:
        return jsonify({"error": validation_error}), 400

    start_time = time.time()

    try:
        send_magic_packet(wake_request["mac_address"])

        if wait_for_device_online(
            wake_request["ip_address"],
            wake_request["timeout_seconds"],
            start_time
        ):
            return build_success_response(start_time)

        return build_timeout_response(wake_request["timeout_seconds"])

    except Exception as e:
        return build_error_response(start_time, e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
