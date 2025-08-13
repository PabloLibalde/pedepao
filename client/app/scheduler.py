import threading, time, datetime, zoneinfo
from typing import Callable

def get_tz(tz_name: str):
    try:
        return zoneinfo.ZoneInfo(tz_name)
    except Exception:
        try:
            sec = -time.timezone
            if time.daylight and time.localtime().tm_isdst:
                sec = -time.altzone
            return datetime.timezone(datetime.timedelta(seconds=sec))
        except Exception:
            return datetime.timezone.utc

class DailyTrigger:
    def __init__(self, hh: int, mm: int, tz_name: str, callback: Callable[[], None]):
        self.hh = hh
        self.mm = mm
        self.tz = get_tz(tz_name)
        self.cb = callback
        self._stop = False
        self._th = threading.Thread(target=self._runner, daemon=True)
        self._th.start()

    def _runner(self):
        while not self._stop:
            now = datetime.datetime.now(self.tz)
            target = now.replace(hour=self.hh, minute=self.mm, second=0, microsecond=0)
            if target <= now:
                target += datetime.timedelta(days=1)
            wait = (target - now).total_seconds()
            while wait > 0 and not self._stop:
                step = min(60, wait)
                time.sleep(step)
                wait -= step
            if self._stop: break
            try:
                self.cb()
            except Exception:
                pass

    def stop(self):
        self._stop = True
