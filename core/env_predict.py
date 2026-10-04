import json, datetime, os, settings

CACHE = settings.LOCAL_ENV_JSON
os.makedirs(os.path.dirname(CACHE), exist_ok=True)

DEFAULT = {
    "date": datetime.date.today().isoformat(),
    "aqi": "Green",        # Green | Amber | Red
    "heatAlert": False,
    "sadTrend": False,
    "lowMoodRisk": 0.12
}

def today() -> dict:
    """Return today’s environment dict (always exists)."""
    # cache fresh?
    if os.path.exists(CACHE):
        with open(CACHE) as f:
            data = json.load(f)
            if data.get("date") == datetime.date.today().isoformat():
                return data
    # placeholder cloud download would go here
    with open(CACHE, "w") as f:
        json.dump(DEFAULT, f)
    return DEFAULT