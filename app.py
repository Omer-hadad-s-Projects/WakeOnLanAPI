from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)
WAKE_ON_LAN_SHELL_PATH = './shells/wake_on_lan_shell.sh'
TIMEOUT = '30'


@app.route('/wake', methods=['POST'])
def wake_device():
    data = request.get_json()
    mac_address = data.get('mac_address')
    ip_address = data.get('ip_address')

    if not mac_address or not ip_address:
        return jsonify({"error": "Both mac_address and target_ip are required."}), 400

    try:
        result = subprocess.run(
            [WAKE_ON_LAN_SHELL_PATH, mac_address, ip_address, TIMEOUT],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output = result.stdout.decode('utf-8')
        exit_code = result.returncode

        return jsonify({"output": output, "exit_code": exit_code}), 200
    except Exception as e:
        error_message = f'Error {str(e)}'
        return error_message, 500


if __name__ == '__main__':
    app.run()
