from datetime import datetime, timezone, timedelta


class ExtensionTracker:
    def __init__(self, max_requests: int, window: timedelta):
        self.max_requests = max_requests
        self.window = window
        self.count = 0
        self.reset_time = datetime.now(timezone.utc) + self.window

    def update(self) -> bool:
        """Try to register a request. Returns True if allowed, False if over limit."""
        now = datetime.now(timezone.utc)

        if now > self.reset_time:
            self.count = 0
            self.reset_time = now + self.window

        if self.count >= self.max_requests:
            return False

        self.count += 1
        return True

    def clear(self):
        """Immediately reset usage."""
        self.count = 0
        self.reset_time = datetime.now(timezone.utc) + self.window


class RateManager:
    def __init__(self, per_ext_max: int, global_max: int, window: timedelta):
        self.per_ext_max = per_ext_max
        self.global_max = global_max
        self.window = window
        self.trackers: dict[str, ExtensionTracker] = {}
        
        # individual tracker for global max
        self.trackers["__total__"] = ExtensionTracker(global_max, window)

    def update(self, ext_id: str) -> tuple[bool, str]:
        """
        Try to register a request for a given extension.
        Returns allowed
        """
        # Update extension tracker
        if ext_id not in self.trackers:
            self.trackers[ext_id] = ExtensionTracker(self.per_ext_max, self.window)
        if not self.trackers[ext_id].update():
            return False

        # Update global tracker
        if not self.trackers["__total__"].update():
            # Roll back extension increment (so counts stay consistent)
            self.trackers[ext_id].count -= 1
            return False

        return True

    def clear(self, ext_id: str | None = None):
        """Reset one extension or all."""
        if ext_id is None:
            for t in self.trackers.values():
                t.clear()
        elif ext_id in self.trackers:
            self.trackers[ext_id].clear()
