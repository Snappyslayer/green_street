"""Create a simple CSV template for measurement results.

Run from the project root:
    python3 experiments/run_experiment.py
"""

from pathlib import Path
import csv
from datetime import datetime, timezone

OUTPUT_FILE = Path("experiments/measurement_results.csv")

rows = [
    {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scenario": "normal_operation",
        "node_id": "light_1",
        "failure_time_s": "0",
        "stale_detected_s": "0",
        "safe_brightness_applied_s": "0",
        "recovery_time_s": "0",
        "notes": "Baseline run; all nodes online.",
    },
    {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scenario": "node_failure",
        "node_id": "light_2",
        "failure_time_s": "0",
        "stale_detected_s": "10",
        "safe_brightness_applied_s": "10",
        "recovery_time_s": "",
        "notes": "Expected safe-default command after stale threshold.",
    },
]

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Measurement CSV created: {OUTPUT_FILE}")
