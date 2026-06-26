"""Digital Twin state manager for simulated smart street lights."""

from __future__ import annotations

from datetime import datetime, timezone
from threading import Lock
from typing import Any

from src.config import BRIGHTNESS_SAFE_DEFAULT, NODE_IDS, STALE_THRESHOLD_SECONDS


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class DigitalTwin:
    """Keeps the latest software-state copy of the lighting infrastructure."""

    def __init__(self) -> None:
        self._lock = Lock()
        self.nodes: dict[str, dict[str, Any]] = {}
        for node_id in NODE_IDS:
            self.nodes[node_id] = {
                "node_id": node_id,
                "status": "unknown",
                "motion": False,
                "ambient": 0,
                "brightness": BRIGHTNESS_SAFE_DEFAULT,
                "last_seen": None,
                "stale": True,
                "last_command_time": None,
            }

    def update_node(self, node_id: str, status: str, motion: bool, ambient: int, brightness: int) -> None:
        with self._lock:
            self.nodes[node_id] = {
                "node_id": node_id,
                "status": status,
                "motion": motion,
                "ambient": ambient,
                "brightness": brightness,
                "last_seen": utc_now_iso(),
                "stale": status != "online",
                "last_command_time": utc_now_iso(),
            }

    def check_stale_nodes(self) -> None:
        now = datetime.now(timezone.utc)
        with self._lock:
            for data in self.nodes.values():
                last_seen = data.get("last_seen")
                if last_seen is None:
                    data["status"] = "unknown"
                    data["stale"] = True
                    data["brightness"] = BRIGHTNESS_SAFE_DEFAULT
                    continue

                last_seen_time = datetime.fromisoformat(last_seen)
                age_seconds = (now - last_seen_time).total_seconds()
                data["age_seconds"] = round(age_seconds, 2)

                if age_seconds > STALE_THRESHOLD_SECONDS:
                    data["status"] = "stale"
                    data["stale"] = True
                    data["brightness"] = BRIGHTNESS_SAFE_DEFAULT
                    data["last_command_time"] = utc_now_iso()

    def get_all_nodes(self) -> dict[str, dict[str, Any]]:
        self.check_stale_nodes()
        with self._lock:
            return {node_id: data.copy() for node_id, data in self.nodes.items()}

    def get_node(self, node_id: str) -> dict[str, Any] | None:
        self.check_stale_nodes()
        with self._lock:
            node = self.nodes.get(node_id)
            return None if node is None else node.copy()

    def get_metrics(self) -> dict[str, Any]:
        nodes = self.get_all_nodes()
        total_nodes = len(nodes)
        stale_nodes = sum(1 for node in nodes.values() if node["stale"])
        online_nodes = total_nodes - stale_nodes
        return {
            "total_nodes": total_nodes,
            "online_nodes": online_nodes,
            "stale_nodes": stale_nodes,
            "stale_threshold_seconds": STALE_THRESHOLD_SECONDS,
            "timestamp": utc_now_iso(),
        }


digital_twin = DigitalTwin()
