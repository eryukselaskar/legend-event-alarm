import json
from datetime import datetime, timedelta, timezone

SERVER_TZ = timezone(timedelta(hours=3))

DAY_NAMES = [
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
]


def load_events(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["events"]


def event_occurs_on_date(event, date_obj):
    days = event["days"]
    weekday = DAY_NAMES[date_obj.weekday()]
    if days == "daily":
        return True
    if days == "daily_except_sunday":
        return weekday != "sunday"
    if isinstance(days, list):
        return weekday in days
    return False


def server_occurrences_near(events, now_server):
    """Yield (event, server_datetime) for every scheduled time on the day
    before, the current day, and the day after (server calendar), so that
    callers can catch occurrences whose alarm offsets cross midnight."""
    for day_delta in (-1, 0, 1):
        date_obj = (now_server + timedelta(days=day_delta)).date()
        for event in events:
            if not event_occurs_on_date(event, date_obj):
                continue
            for time_str in event["times"]:
                hour, minute = (int(x) for x in time_str.split(":"))
                event_dt = datetime(
                    date_obj.year, date_obj.month, date_obj.day,
                    hour, minute, tzinfo=SERVER_TZ,
                )
                yield event, event_dt


def next_upcoming_event(events, now_utc, muted_names=()):
    """Return (name, event_dt_server) for the nearest future occurrence,
    scanning up to a week ahead so weekly events are found too."""
    now_server = now_utc.astimezone(SERVER_TZ)
    for day_delta in range(0, 8):
        date_obj = (now_server + timedelta(days=day_delta)).date()
        day_best = None
        for event in events:
            if event["name"] in muted_names:
                continue
            if not event_occurs_on_date(event, date_obj):
                continue
            for time_str in event["times"]:
                hour, minute = (int(x) for x in time_str.split(":"))
                event_dt = datetime(
                    date_obj.year, date_obj.month, date_obj.day,
                    hour, minute, tzinfo=SERVER_TZ,
                )
                if event_dt <= now_server:
                    continue
                if day_best is None or event_dt < day_best[1]:
                    day_best = (event["name"], event_dt)
        if day_best:
            return day_best
    return None


def todays_events_local(events, now_server, muted_names=()):
    """Return today's (server-day) events as (local_datetime, name) sorted by time."""
    date_obj = now_server.date()
    result = []
    for event in events:
        if event["name"] in muted_names:
            continue
        if not event_occurs_on_date(event, date_obj):
            continue
        for time_str in event["times"]:
            hour, minute = (int(x) for x in time_str.split(":"))
            event_dt = datetime(
                date_obj.year, date_obj.month, date_obj.day,
                hour, minute, tzinfo=SERVER_TZ,
            )
            result.append((event_dt.astimezone(), event["name"]))
    result.sort(key=lambda item: item[0])
    return result
