"""MQTT node simulator for Green Street.

Run on macOS:
    python3 -m src.node_simulator

Stop with Ctrl+C.
"""

import argparse
import json
import random
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

from src.config import MQTT_BROKER, MQTT_PORT, NODE_IDS, PUBLISH_INTERVAL_SECONDS


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def create_sensor_message(node_id: str, offline_node: str | None) -> dict:
    if offline_node == node_id:
        return {
            "node_id": node_id,
            "status": "offline",
            "motion": False,
            "ambient": 0,
            "timestamp": now_iso(),
        }

    return {
        "node_id": node_id,
        "status": "online",
        "motion": random.choice([True, False]),
        "ambient": random.randint(10, 90),
        "timestamp": now_iso(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate MQTT smart street-light nodes.")
    parser.add_argument("--offline-node", default=None, help="Node to simulate as offline, example: light_2")
    args = parser.parse_args()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    print("Green Street node simulator started.")
    print(f"Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print("Stop with Ctrl+C. Use --offline-node light_2 to simulate failure.")

    try:
        while True:
            for node_id in NODE_IDS:
                message = create_sensor_message(node_id, args.offline_node)
                topic = f"greenstreet/{node_id}/status"
                payload = json.dumps(message)
                client.publish(topic, payload)
                print(f"Published {topic}: {payload}")
            time.sleep(PUBLISH_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nNode simulator stopped.")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
