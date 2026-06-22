import json
import time
import threading
from fastapi import FastAPI
import paho.mqtt.client as mqtt

app = FastAPI(title="Green Street Digital Twin API")

twin_state = {}
state_lock = threading.Lock() # FIX: Added thread synchronization

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = json.loads(msg.payload.decode())
    parts = topic.split('/')
    
    if len(parts) >= 3:
        node_id = parts[2]
        with state_lock:
            if node_id not in twin_state:
                twin_state[node_id] = {"status": "UNKNOWN", "last_seen": 0, "brightness": "DEFAULT"}
            
            twin_state[node_id]["last_seen"] = time.time()
            
            if "status" in topic:
                twin_state[node_id]["status"] = payload["status"]
                if payload["status"] == "OFFLINE":
                    twin_state[node_id]["brightness"] = "SAFE_DEFAULT_60"
            elif "events" in topic:
                if payload["event"] == "MOTION_DETECTED":
                    twin_state[node_id]["brightness"] = "HIGH_100"
                elif payload["event"] == "NO_MOTION":
                    twin_state[node_id]["brightness"] = "LOW_20"

def mqtt_shadow():
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.subscribe("street/nodes/#")
    client.loop_forever()

threading.Thread(target=mqtt_shadow, daemon=True).start()

@app.get("/api/grid")
def get_grid_state():
    with state_lock:
        # FIX: Removed independent timeout logic to prevent state drift
        return {"active_nodes": len(twin_state), "nodes": twin_state}
