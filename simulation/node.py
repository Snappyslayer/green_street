import time
import json
import random
import paho.mqtt.client as mqtt

NODE_ID = "node_street1_01"
BROKER = "localhost"

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

# FIX: MQTT Last Will and Testament (LWT) configured here
client.will_set(f"street/nodes/{NODE_ID}/status", json.dumps({"status": "OFFLINE"}), qos=1, retain=True)
client.connect(BROKER, 1883, 60)
client.loop_start()

try:
    while True:
        client.publish(f"street/nodes/{NODE_ID}/status", json.dumps({"status": "ONLINE"}), qos=1)
        
        # FIX: Added NO_MOTION event to clear the state lock
        if random.random() < 0.3:
            client.publish(f"street/nodes/{NODE_ID}/events", json.dumps({"event": "MOTION_DETECTED"}), qos=1)
            time.sleep(4) 
            client.publish(f"street/nodes/{NODE_ID}/events", json.dumps({"event": "NO_MOTION"}), qos=1)
        
        time.sleep(5)
except KeyboardInterrupt:
    client.publish(f"street/nodes/{NODE_ID}/status", json.dumps({"status": "OFFLINE"}), qos=1, retain=True)
    client.disconnect()
