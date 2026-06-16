import time
import random
import json
import paho.mqtt.client as mqtt

NODE_ID = "node_street1_01"
BROKER = "localhost"
PORT = 1883
TOPIC_STATUS = f"street/nodes/{NODE_ID}/status"
TOPIC_EVENTS = f"street/nodes/{NODE_ID}/events"

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

print(f"Connecting to MQTT broker at {BROKER}...")
client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    while True:
        # 1. Send periodic Heartbeat (Status)
        status_payload = {"status": "ONLINE", "timestamp": time.time()}
        client.publish(TOPIC_STATUS, json.dumps(status_payload), qos=1, retain=True)
        print(f"[{NODE_ID}] Sent Heartbeat")

        # 2. Simulate random motion detection events
        if random.random() > 0.6:
            event_payload = {
                "event": "MOTION_DETECTED",
                "ambient_light": random.randint(10, 40), # Low lux
                "timestamp": time.time()
            }
            client.publish(TOPIC_EVENTS, json.dumps(event_payload), qos=1)
            print(f"[{NODE_ID}] 🚶 Motion detected! Event published.")
        
        time.sleep(5) # Send updates every 5 seconds

except KeyboardInterrupt:
    print("\nDisconnecting node gracefully...")
    # Clean up state on exit by marking node as offline
    client.publish(TOPIC_STATUS, json.dumps({"status": "OFFLINE", "timestamp": time.time()}), qos=1, retain=True)
    client.loop_stop()
    client.disconnect()
