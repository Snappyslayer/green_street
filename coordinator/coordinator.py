import time
import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
HEARTBEAT_TIMEOUT = 12.0 # Mark stale if no heartbeat within 12 seconds

# System State Trackers
node_states = {}

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = json.loads(msg.payload.decode())
    
    # Extract Node ID from topic string
    parts = topic.split('/')
    node_id = parts[2]
    
    if node_id not in node_states:
        node_states[node_id] = {"status": "UNKNOWN", "last_seen": 0, "brightness": "DEFAULT"}

    if "status" in topic:
        node_states[node_id]["status"] = payload["status"]
        node_states[node_id]["last_seen"] = time.time()
        if payload["status"] == "OFFLINE":
            evaluate_node_policy(node_id, "TIMEOUT")
            
    elif "events" in topic:
        node_states[node_id]["last_seen"] = time.time()
        if payload["event"] == "MOTION_DETECTED" and node_states[node_id]["status"] == "ONLINE":
            evaluate_node_policy(node_id, "MOTION")

def evaluate_node_policy(node_id, trigger):
    state = node_states[node_id]
    current_time = time.time()
    
    # Check for staleness timeout
    if current_time - state["last_seen"] > HEARTBEAT_TIMEOUT or state["status"] == "OFFLINE":
        state["brightness"] = "SAFE_DEFAULT_60"
        print(f"⚠️ [CRITICAL] {node_id} is UNREACHABLE. Fallback to Safe-Default (60% Brightness).")
    elif trigger == "MOTION":
        state["brightness"] = "HIGH_100"
        print(f"💡 [ADAPTIVE] Motion at {node_id}. Setting Brightness to 100%.")
    else:
        # Default idle adaptive dimming
        state["brightness"] = "LOW_20"
        print(f"🌙 [ADAPTIVE] Idle at {node_id}. Dimming to 20%.")

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.subscribe("street/nodes/+/status")
client.subscribe("street/nodes/+/events")

client.loop_start()
print("Adaptive Coordinator running. Monitoring network...")

try:
    while True:
        # Periodic check for silent/dead nodes that haven't explicitly said they are offline
        now = time.time()
        for node_id in list(node_states.keys()):
            if now - node_states[node_id]["last_seen"] > HEARTBEAT_TIMEOUT and node_states[node_id]["brightness"] != "SAFE_DEFAULT_60":
                evaluate_node_policy(node_id, "TIMEOUT")
        time.sleep(2)

except KeyboardInterrupt:
    print("\nShutting down coordinator...")
    client.loop_stop()
    client.disconnect()
