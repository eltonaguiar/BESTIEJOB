"""Per-host circuit breaker and politeness delay.

A sweep over ~1,000 arbitrary employer hosts will hit dead domains, parked
pages and WAFs. Three counters per host are enough to stop burning wall-clock
on a host that has already refused us.
"""
from __future__ import annotations

import random
import threading
import time


class HostGate:
    def __init__(self, *, max_failures: int = 4, quarantine_s: float = 300.0,
                 min_interval_s: float = 1.0) -> None:
        self.max_failures = max_failures
        self.quarantine_s = quarantine_s
        self.min_interval_s = min_interval_s
        self._lock = threading.Lock()
        self._failures: dict[str, int] = {}
        self._until: dict[str, float] = {}
        self._last: dict[str, float] = {}

    def available(self, host: str) -> bool:
        with self._lock:
            until = self._until.get(host, 0.0)
            return time.monotonic() >= until

    def wait(self, host: str) -> float:
        """Sleep the remainder of the polite interval. Returns seconds slept."""
        with self._lock:
            last = self._last.get(host)
            now = time.monotonic()
            delay = 0.0
            if last is not None:
                delay = (last + self.min_interval_s) - now
            if delay > 0:
                delay += random.uniform(0, 0.35)   # jitter, not a metronome
            self._last[host] = now + max(delay, 0.0)
        if delay > 0:
            time.sleep(delay)
        return max(delay, 0.0)

    def record(self, host: str, ok: bool) -> None:
        with self._lock:
            if ok:
                self._failures.pop(host, None)
                return
            n = self._failures.get(host, 0) + 1
            self._failures[host] = n
            if n >= self.max_failures:
                self._until[host] = time.monotonic() + self.quarantine_s

    def is_quarantined(self, host: str) -> bool:
        with self._lock:
            return time.monotonic() < self._until.get(host, 0.0)

    def failures(self, host: str) -> int:
        with self._lock:
            return self._failures.get(host, 0)
