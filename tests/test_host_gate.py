import time

from scripts.referral.host_gate import HostGate


def test_quarantines_after_max_failures():
    gate = HostGate(max_failures=3, quarantine_s=60, min_interval_s=0)
    for _ in range(2):
        gate.record("dead.example", ok=False)
    assert gate.available("dead.example")
    gate.record("dead.example", ok=False)
    assert not gate.available("dead.example")
    assert gate.is_quarantined("dead.example")


def test_success_resets_counter():
    gate = HostGate(max_failures=2, quarantine_s=60, min_interval_s=0)
    gate.record("flaky.example", ok=False)
    gate.record("flaky.example", ok=True)
    gate.record("flaky.example", ok=False)
    assert gate.available("flaky.example")


def test_wait_is_zero_when_interval_already_elapsed():
    gate = HostGate(min_interval_s=0.0)
    assert gate.wait("a.example") == 0.0
    assert gate.wait("a.example") == 0.0


def test_wait_enforces_interval():
    gate = HostGate(min_interval_s=0.2)
    gate.wait("b.example")
    slept = gate.wait("b.example")
    assert slept > 0.1
