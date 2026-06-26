# Green Street: A Verified Digital Twin for Adaptive Smart Lighting Infrastructure

This project implements a simulated adaptive smart street lighting system using MQTT, a central coordinator, a Digital Twin REST API, and Spin/Promela verification.

## Components

- `src/node_simulator.py` simulates smart street-light nodes.
- `src/coordinator.py` contains adaptive brightness rules.
- `src/digital_twin.py` stores the live Digital Twin state.
- `src/api_server.py` runs the REST API and MQTT listener.
- `verification/coordinator_model.pml` models the coordinator for Spin verification.
- `experiments/run_experiment.py` creates a starter measurement CSV.

## macOS Setup

### 1. Open Terminal in this project folder

After extracting the ZIP on your Desktop:

```bash
cd ~/Desktop/green-street-digital-twin-mac
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python libraries

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

### 4. Install Mosquitto MQTT broker

If Homebrew is installed:

```bash
brew install mosquitto
brew services start mosquitto
```

If you do not have Homebrew yet, install Homebrew first from the official Homebrew website.

### 5. Run the REST API

Open Terminal 1:

```bash
source .venv/bin/activate
uvicorn src.api_server:app --reload
```

Open this in the browser:

```text
http://127.0.0.1:8000/docs
```

### 6. Run the node simulator

Open Terminal 2:

```bash
cd ~/Desktop/green-street-digital-twin-mac
source .venv/bin/activate
python3 -m src.node_simulator
```

Then check:

```text
http://127.0.0.1:8000/nodes
http://127.0.0.1:8000/metrics
```

### 7. Simulate a failure

Stop the simulator with `Ctrl+C`, then run:

```bash
python3 -m src.node_simulator --offline-node light_2
```

The coordinator should command safe-default brightness for the offline/stale node.

## Verification with Spin/Promela

After installing Spin and GCC on macOS:

```bash
spin -a verification/coordinator_model.pml
gcc -o pan pan.c
./pan -a
```

## GitHub Upload

You can upload manually without Git:

1. Open GitHub.
2. Create repository: `green-street-digital-twin`.
3. Click **Add file**.
4. Click **Upload files**.
5. Drag the project files/folders.
6. Commit changes.

## Report Results to Include

- API `/docs` page.
- `/nodes` response showing live Digital Twin state.
- Failure scenario with offline/stale node.
- Measurement CSV.
- Spin verification result.
