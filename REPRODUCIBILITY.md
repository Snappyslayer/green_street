# Reproducibility Guide

To execute this project and reproduce the environment, follow these steps:

## 1. Prerequisites
* Python 3.9+
* Mosquitto MQTT Broker (running locally on port 1883)
* Spin Verifier (`brew install spin` on macOS or via apt)

## 2. Environment Setup
`python3 -m venv venv`
`source venv/bin/activate`
`pip install paho-mqtt fastapi uvicorn`

## 3. Execution (Run in separate terminal tabs)
1. **Start Coordinator:** `python coordinator/coordinator.py`
2. **Start Node:** `python simulation/node.py`
3. **Start Digital Twin:** `uvicorn digital_twin.app:app --reload`
4. **View Twin:** Navigate to `http://127.0.0.1:8000/api/grid`

## 4. Run Formal Verification
`spin -a verification/coordinator.pml`
`cc -o pan pan.c`
`./pan -a -N safety`
`./pan -a -N liveness`
`./pan -a -N recovery`
*(All LTL proofs should output errors: 0)*
