# Green Street: Verified Digital Twin

**Adaptive Smart Lighting Infrastructure with Formal Verification**

This project implements an event-driven Smart City lighting infrastructure. It uses MQTT to communicate with simulated edge devices, features a real-time FastAPI Digital Twin to monitor the grid, and utilizes formal LTL verification (Promela/Spin) to mathematically prove the system's safety and liveness during hardware failures.

## Key Features
* **MQTT Edge Simulation:** Streetlight nodes publish telemetry and utilize Last Will and Testament (LWT) for instant crash detection.
* **Adaptive Coordinator:** Central logic that dynamically adjusts brightness based on motion events and forces a safe-fallback state (`SAFE_DEFAULT_60`) during network failures.
* **REST API Digital Twin:** A FastAPI server that silently shadows the MQTT broker, providing real-time grid state without polling physical devices.
* **Formal Verification:** Spin/Promela models that mathematically prove strict safety bounds, liveness, and bounded recovery.

## Documentation
Please refer to the following files for execution and compliance details:
* [Reproducibility Guide](./REPRODUCIBILITY.md) - Instructions for environment setup, running the simulation, and executing the formal verification proofs.
* [Generative AI Disclosure](./AI_DISCLOSURE.md) - Details on how Generative AI tools were utilized, modified, and validated during development.
* [Measurement Report](./report/measurement_report.md) - Latency and failover performance metrics for the LWT implementation.
