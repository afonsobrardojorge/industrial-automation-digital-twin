from src.model import AutomationCell, MachineState


def test_automatic_mode_starts_conveyor() -> None:
    cell = AutomationCell()
    cell.start()
    assert cell.state is MachineState.AUTOMATIC
    assert cell.conveyor_motor is True


def test_quality_counters_are_updated() -> None:
    cell = AutomationCell()
    cell.start()
    cell.process_part(quality_ok=True)
    cell.process_part(quality_ok=False)
    assert cell.total_parts == 2
    assert cell.good_parts == 1
    assert cell.rejected_parts == 1
    assert cell.metrics["yield_rate"] == 50.0


def test_emergency_stop_forces_safe_outputs() -> None:
    cell = AutomationCell()
    cell.start()
    cell.emergency_stop()
    assert cell.state is MachineState.EMERGENCY_STOP
    assert cell.conveyor_motor is False
    assert cell.reject_cylinder is False


def test_manual_mode_requires_manual_state() -> None:
    cell = AutomationCell()
    cell.start(manual_mode=True)
    cell.set_manual_outputs(conveyor=True, reject=True)
    assert cell.conveyor_motor is True
    assert cell.reject_cylinder is True


def test_maintenance_threshold_creates_alert() -> None:
    cell = AutomationCell(maintenance_threshold=2)
    cell.start()
    cell.process_part(quality_ok=True)
    cell.process_part(quality_ok=True)
    assert cell.maintenance_required is True
    assert any(event.kind == "maintenance" for event in cell.events)
