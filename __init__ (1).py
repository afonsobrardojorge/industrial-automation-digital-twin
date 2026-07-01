"""Generate a deterministic telemetry log for the automation-cell demo."""

from __future__ import annotations

import json
from pathlib import Path

from src.model import AutomationCell


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    cell = AutomationCell(maintenance_threshold=4)

    cell.start()
    cell.process_part(quality_ok=True)
    cell.process_part(quality_ok=True)
    cell.process_part(quality_ok=False)
    cell.process_part(quality_ok=True)
    cell.stop()
    cell.start(manual_mode=True)
    cell.set_manual_outputs(conveyor=True, reject=False)
    cell.emergency_stop()
    cell.reset_fault()

    events_path = DATA_DIR / "demo_events.jsonl"
    metrics_path = DATA_DIR / "demo_metrics.json"

    with events_path.open("w", encoding="utf-8") as fh:
        for event in cell.events:
            fh.write(json.dumps(event.as_dict()) + "\n")

    metrics_path.write_text(json.dumps(cell.metrics, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {len(cell.events)} events to {events_path.relative_to(ROOT)}")
    print(json.dumps(cell.metrics, indent=2))


if __name__ == "__main__":
    main()
