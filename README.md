# Wake On Lan API

An API for sending Wake-on-LAN commands to devices on your local network.

## Requirements

- **Wake-on-LAN**: Ensure the device has Wake-on-LAN (WoL) enabled in its BIOS settings.
- **Static IP**: The device must have a static IP address assigned.

## Initial Setup

### 1. Add `.env` File

Create a `.env` file in the project root directory and define the port for the service. For example:

```
APP_PORT=5000
```

### 2. Build Docker Image

Build the Docker image on the machine hosting the API using the following command:

```
docker build -t <your_image_name> .
```

Replace `<your_image_name>` with a name you choose for your Docker image.

### 3. Run Container in Network Host Mode

Start the container with the `--network host` option to ensure proper network functionality:

```
docker run --network host -t <your_image_name>
```

Replace `<your_image_name>` with the name of the Docker image you built in the previous step.

### 4. Send Request to Wake Device

Send a POST request to wake the device.

- **Request URL**: `http://host_address:port_defined_in_env/wake`
- **Method**: POST
- **Payload** (JSON format):

```
{
  "mac_address": "<device_mac_address>",
  "ip_address": "<device_ip>"
}
```

## Example

Here’s an example of how to send a request using `curl`:

```
curl -X POST http://localhost:5000/wake \
     -H "Content-Type: application/json" \
     -d '{"mac_address": "00:11:22:33:44:55", "ip_address": "192.168.0.14"}'
```
