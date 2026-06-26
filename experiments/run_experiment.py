# run_experiment.py
# Simple measurement script for Green Street Digital Twin.
# It queries the REST API and stores current metrics in a CSV file.

import csv
import time
from datetime import datetime
from pathlib import Path

import requests


API_BASE_URL = "http://127.0.0.1:8000"
OUTPUT_FILE = Path("experiments/measurement_results.csv")


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "timestamp",
            "total_nodes",
            "online_nodes",
            "stale_nodes",
            "stale_threshold_seconds"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        print("Collecting measurements from Digital Twin API.")
        print("Press Ctrl+C to stop.")

        try:
            while True:
                response = requests.get(f"{API_BASE_URL}/metrics", timeout=5)
                metrics = response.json()

                row = {
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "total_nodes": metrics["total_nodes"],
                    "online_nodes": metrics["online_nodes"],
                    "stale_nodes": metrics["stale_nodes"],
                    "stale_threshold_seconds": metrics["stale_threshold_seconds"]
                }

                writer.writerow(row)
                csvfile.flush()

                print(row)
                time.sleep(2)

        except KeyboardInterrupt:
            print(f"\nMeasurement stopped. Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
