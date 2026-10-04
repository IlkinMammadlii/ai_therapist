import settings
from copernicus_s5p import get_env_dict

_cached = None

def today():
    global _cached
    if not _cached:
        _cached = get_env_dict(settings.CDSE_BBOX)
    return _cached
