"""In-memory sliding-window rate limiter (R14.7).

Single-process only: counts live in this process's memory, so each worker or instance keeps
its own window. A deployment with more than one API process needs a shared store (for
example Redis or a database table) behind the same ``hit`` interface.
"""

from __future__ import annotations

import math
import threading
import time
from collections import deque
from collections.abc import Callable


class SlidingWindowRateLimiter:
    def __init__(
        self,
        max_requests: int,
        window_seconds: float,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._clock = clock
        self._hits: dict[str, deque[float]] = {}
        self._lock = threading.Lock()

    def hit(self, key: str) -> int | None:
        """Record one request for ``key``.

        Returns None when allowed, or the whole seconds to wait when the limit is reached.
        A rejected request is not recorded.
        """
        now = self._clock()
        with self._lock:
            hits = self._hits.setdefault(key, deque())
            cutoff = now - self.window_seconds
            while hits and hits[0] <= cutoff:
                hits.popleft()
            if len(hits) >= self.max_requests:
                return max(1, math.ceil(hits[0] + self.window_seconds - now))
            hits.append(now)
            return None

    def reset(self) -> None:
        with self._lock:
            self._hits.clear()
