"""FastAPI REST service and MQTT listener for the Green Street Digital Twin.

Run on macOS:
    uvicorn src.api_server:app --reload
"""

import json
import threading

import paho.mqtt.client as mqtt
from fastapi import FastAPI

from src.config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC
from src.coordinator import decide_brightness
from src.digital_twin import digital_twin

app = FastAPI(
    title="Green Street Digital Twin API",
    description="REST API for monitoring adaptive smart street lighting nodes.",
    version="1.0.0",
)


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Connected to MQTT broker.")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to {MQTT_TOPIC}")
    else:
        print(f"Failed to connect to MQTT broker. Code: {reason_code}")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        node_id = data["node_id"]
        status = data.get("status", "unknown")
        motion = bool(data.get("motion", False))
        ambient = int(data.get("ambient", 0))
        brightness = decide_brightness(status, motion, ambient)
        digital_twin.update_node(node_id, status, motion, ambient, brightness)
        print(f"Twin updated: {node_id} status={status} brightness={brightness}")
    except Exception as exc:
        print(f"Error processing MQTT message: {exc}")


def start_mqtt_listener() -> None:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()


@app.on_event("startup")
def startup_event() -> None:
    thread = threading.Thread(target=start_mqtt_listener, daemon=True)
    thread.start()


@app.get("/")
def home():
    return {
        "message": "Green Street Digital Twin API is running",
        "docs": "Open /docs to test the API",
    }


@app.get("/nodes")
def get_nodes():
    return digital_twin.get_all_nodes()


@app.get("/nodes/{node_id}")
def get_node(node_id: str):
    node = digital_twin.get_node(node_id)
    if node is None:
        return {"error": "Node not found"}
    return node


@app.get("/metrics")
def get_metrics():
    return digital_twin.get_metrics()


@app.get("/health")
def health():
    return {"status": "running"}
