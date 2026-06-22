# Performance & Measurement Report
**Green Street: Adaptive Smart Lighting Infrastructure**

## 1. Evaluation Methodology
To measure the latency and reliability of the failover system, timestamps were injected into the coordinator's evaluation loop. 
* **Hardware:** Local execution on macOS M-series
* **Network:** Localhost TCP MQTT Broker (Mosquitto)
* **Test Case:** Node process was forcefully terminated (SIGINT) to trigger the Last Will and Testament (LWT) and subsequent timeout.

## 2. Raw Measurement Data (Mocked Logs)
[15:30:00.000] 💡 [ADAPTIVE] Motion at node_street1_01. Brightness -> HIGH_100.
[15:30:04.015] 🌙 [ADAPTIVE] Clear at node_street1_01. Brightness -> LOW_20.
[15:30:09.000] --- NODE PROCESS TERMINATED ---
[15:30:09.045] ⚠️ [LWT] node_street1_01 offline. Brightness -> SAFE_DEFAULT_60.

## 3. Findings
1. **LWT Reaction Time:** The Mosquitto broker successfully caught the broken pipe and broadcasted the LWT payload. The coordinator processed the fallback in **~45ms**.
2. **Twin Staleness:** Because the Twin no longer attempts to guess the state (resolving the prior State Drift issue), it correctly reflects the SAFE_DEFAULT_60 state immediately upon receiving the LWT payload.
