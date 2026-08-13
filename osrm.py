import urllib.request
import json

OSRM_BASE = "http://router.project-osrm.org"

def get_duration_matrix(stops):
    """Returns an n x n matrix of driving durations in MINUTES between stops."""
    coords = ";".join(f"{stop.lng},{stop.lat}" for stop in stops)  # lng,lat order
    url = f"{OSRM_BASE}/table/v1/driving/{coords}?annotations=duration"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read())
    except Exception as e:
        raise RuntimeError(f"OSRM request failed: {e}") from e

    if data.get("code") != "Ok":
        raise RuntimeError(f"OSRM error: {data.get('code')} - {data.get('message', '')}")

    durations_seconds = data["durations"]

    n = len(durations_seconds)
    for i in range(n):
        for j in range(n):
            if durations_seconds[i][j] is None:
                raise RuntimeError(f"OSRM found no route between stop {i} and stop {j}")

    return [[s / 60.0 for s in row] for row in durations_seconds]
