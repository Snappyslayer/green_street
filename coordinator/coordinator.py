import paho.mqtt.client as mqtt
import json
import time
import threading

nodes = {}
TIMEOUT = 12.0

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = json.loads(msg.payload.decode())
    node_id = topic.split('/')[2]
    
    if node_id not in nodes:
        nodes[node_id] = {"last_seen": time.time(), "status": "UNKNOWN", "brightness": "LOW_20"}
        
    nodes[node_id]["last_seen"] = time.time()
    
    if "status" in topic:
        nodes[node_id]["status"] = payload["status"]
        if payload["status"] == "OFFLINE":
            nodes[node_id]["brightness"] = "SAFE_DEFAULT_60"
            print(f"⚠️ [LWT] {node_id} offline. Brightness -> SAFE_DEFAULT_60.")
            
    elif "events" in topic:
        # FIX: Handle NO_MOTION to prevent state lock
        if payload["event"] == "MOTION_DETECTED":
            nodes[node_id]["brightness"] = "HIGH_100"
            print(f"💡 [ADAPTIVE] Motion at {node_id}. Brightness -> HIGH_100.")
        elif payload["event"] == "NO_MOTION":
            nodes[node_id]["brightness"] = "LOW_20"
            print(f"🌙 [ADAPTIVE] Clear at {node_id}. Brightness -> LOW_20.")

def monitor_timeouts():
    while True:
        now = time.time()
        for node_id, state in nodes.items():
            if state["status"] == "ONLINE" and (now - state["last_seen"]) > TIMEOUT:
                state["status"] = "OFFLINE"
                state["brightness"] = "SAFE_DEFAULT_60"
                print(f"⚠️ [TIMEOUT] {node_id} silent. Brightness -> SAFE_DEFAULT_60.")
        time.sleep(2)

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.subscribe("street/nodes/#")

threading.Thread(target=monitor_timeouts, daemon=True).start()
client.loop_forever()
