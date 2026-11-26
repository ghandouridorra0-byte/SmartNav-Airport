
import json
import asyncio
import threading

import paho.mqtt.client as mqtt

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware


# ==================================
# CONFIGURATION
# ==================================

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "smartnav/airport/measurements"

ANCHORS = {
    "anchor01": {"x": 100, "y": 100},
    "anchor02": {"x": 400, "y": 100},
    "anchor03": {"x": 250, "y": 350}
}

# ==================================
# FASTAPI
# ==================================

app = FastAPI(title="SmartNav Airport API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

latest_measurements = {}
latest_locations = {}
connected_clients = set()

data_lock = threading.Lock()
event_loop = None


# ==================================
# WEBSOCKET
# ==================================

async def broadcast(data):

    disconnected = []

    for client in list(connected_clients):
        try:
            await client.send_json(data)
        except Exception:
            disconnected.append(client)

    for client in disconnected:
        connected_clients.discard(client)


# ==================================
# POSITIONING ENGINE
# ==================================

def process_measurement(data):

    user_id = data.get("user_id", "user01")
    anchor_id = data.get("anchor_id")
    rssi = data.get("rssi")

    if anchor_id not in ANCHORS:
        return None

    if not isinstance(rssi, (int, float)):
        return None

    with data_lock:

        if user_id not in latest_measurements:
            latest_measurements[user_id] = {}

        latest_measurements[user_id][anchor_id] = {
            "rssi": rssi,
            "timestamp": data.get("timestamp")
        }

        measurements = latest_measurements[user_id]

        strongest_anchor = max(
            measurements,
            key=lambda key: measurements[key]["rssi"]
        )

        position = ANCHORS[strongest_anchor]

        result = {
            "user_id": user_id,
            "anchor_id": strongest_anchor,
            "x": position["x"],
            "y": position["y"],
            "rssi": measurements[strongest_anchor]["rssi"],
            "method": "Nearest Anchor"
        }

        latest_locations[user_id] = result

    return result


# ==================================
# MQTT CALLBACKS
# ==================================

def on_connect(client, userdata, flags, reason_code, properties):

    print("MQTT connected:", reason_code)

    client.subscribe(MQTT_TOPIC)

    print("Subscribed to:", MQTT_TOPIC)


def on_message(client, userdata, message):

    try:

        data = json.loads(message.payload.decode())

        print("MQTT DATA:", data)

        result = process_measurement(data)

        if result and event_loop:

            asyncio.run_coroutine_threadsafe(
                broadcast(result),
                event_loop
            )

    except Exception as error:

        print("Message error:", error)


# ==================================
# MQTT CLIENT
# ==================================

mqtt_client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="smartnav_backend"
)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


# ==================================
# API ROUTES
# ==================================

@app.get("/")
def home():

    return {
        "project": "SmartNav Airport",
        "status": "running"
    }


@app.get("/api/status")
def status():

    return {
        "backend": "online",
        "mqtt_broker": MQTT_BROKER,
        "mqtt_topic": MQTT_TOPIC
    }


@app.get("/api/anchors")
def get_anchors():

    return ANCHORS


@app.get("/api/location/{user_id}")
def get_location(user_id: str):

    with data_lock:
        return latest_locations.get(
            user_id,
            {"message": "No location available"}
        )


# ==================================
# WEBSOCKET ROUTE
# ==================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    connected_clients.add(websocket)

    try:

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:

        connected_clients.discard(websocket)


# ==================================
# STARTUP / SHUTDOWN
# ==================================

@app.on_event("startup")
async def startup():

    global event_loop

    event_loop = asyncio.get_running_loop()

    print("Starting SmartNav Airport...")

    mqtt_client.connect(
        MQTT_BROKER,
        MQTT_PORT,
        60
    )

    mqtt_client.loop_start()


@app.on_event("shutdown")
async def shutdown():

    mqtt_client.loop_stop()
    mqtt_client.disconnect()

    print("SmartNav Airport stopped.")
