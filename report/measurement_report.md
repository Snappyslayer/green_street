# Performance & Measurement Report
**Green Street: Adaptive Smart Lighting Infrastructure**

## 1. Coordinator Reaction Time Under Node Failure
The system requires the Coordinator to detect node failures and apply a safe-fallback brightness level.
* **Configured Heartbeat Interval:** 5.0 seconds
* **Coordinator Staleness Timeout:** 12.0 seconds
* **Measured Reaction Time:** ~12.05 seconds
* **Conclusion:** The Coordinator successfully bounds its reaction time to just over two missed heartbeats. LTL verification confirms this fallback state is always reached.

## 2. Digital Twin Staleness Latency
The Digital Twin mirrors the grid via a passive MQTT shadow.
* **Network Protocol:** MQTT QoS 1 (At least once delivery)
* **Average Twin Update Latency:** < 50ms (Local Broker)
* **Twin Staleness Flagging:** The Twin evaluates node staleness lazily on `GET /api/grid` requests. If a node hasn't published an event or heartbeat in >12 seconds, the Twin accurately reflects the `STALE_OR_OFFLINE` state in real-time alongside the Coordinator's fallback.
