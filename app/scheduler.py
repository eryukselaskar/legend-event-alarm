import threading
import time
from datetime import datetime, timedelta, timezone

from . import events as events_mod
from .i18n import t

TICK_SECONDS = 15
FIRE_WINDOW_SECONDS = 60
OFFSETS = ((10, "notify_10"), (5, "notify_5"), (1, "notify_1"))


class Scheduler:
    def __init__(self, events, get_language, on_notify, get_muted=lambda: (), on_tick=None):
        self.events = events
        self.get_language = get_language
        self.on_notify = on_notify
        self.get_muted = get_muted
        self.on_tick = on_tick
        self._fired = set()
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop.set()

    def _run(self):
        while not self._stop.is_set():
            self._check_once()
            self._prune_fired()
            if self.on_tick:
                self.on_tick()
            self._stop.wait(TICK_SECONDS)

    def _check_once(self):
        now_utc = datetime.now(timezone.utc)
        now_server = now_utc.astimezone(events_mod.SERVER_TZ)
        muted = self.get_muted()
        for event, event_dt in events_mod.server_occurrences_near(self.events, now_server):
            if event["name"] in muted:
                continue
            for minutes_before, key in OFFSETS:
                trigger_dt = event_dt - timedelta(minutes=minutes_before)
                fired_key = (event["name"], event_dt.isoformat(), minutes_before)
                if fired_key in self._fired:
                    continue
                delta = (now_utc - trigger_dt).total_seconds()
                if 0 <= delta < FIRE_WINDOW_SECONDS:
                    self._fired.add(fired_key)
                    message = t(self.get_language(), key, name=event["name"])
                    self.on_notify(t(self.get_language(), "app_title"), message)

    def _prune_fired(self):
        if len(self._fired) < 500:
            return
        now_utc = datetime.now(timezone.utc)
        cutoff = now_utc - timedelta(days=2)
        self._fired = {
            key for key in self._fired
            if datetime.fromisoformat(key[1]) > cutoff
        }
