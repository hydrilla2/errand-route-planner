# Here is the documentation link !!!!
https://docs.google.com/document/d/1VsX1iH2Yf3YJze_CIb6DqSsxK3hcTKDe/edit?usp=sharing&ouid=104687013512495232140&rtpof=true&sd=true

# Errand Route Planner

Given a set of stops, finds the fastest driving order to visit them (exact solver, real road durations via OSRM), and delivers the result to Google Maps for navigation.

## Prerequisites

   fastapi==0.141.1
   uvicorn==0.52.1
   starlette==1.5.0
   httpx2==2.10.0

## Running it

Two things need to run: the backend API, and the frontend page.

**1. Start the backend** (in this folder):
```
python -m uvicorn main:app --reload
```
This serves the API at `http://127.0.0.1:8000`. Leave this terminal running. You can confirm it's up by visiting `http://127.0.0.1:8000/docs` (interactive API docs).

**2. Open the frontend:**
Open `page.html` directly in a browser (double-click it, or `start page.html` on Windows). No build step or server needed for the frontend — it's a static file that calls the backend at `http://127.0.0.1:8000`.

## Using the app

- Add stops by searching an address or clicking the map
- Choose how the route should end: return to the start, end anywhere, or end at a specific stop.
- Click "Plan route" to get the optimised visiting order, the optimised vs. naive travel time, and a link to open the route in Google Maps.

## Running the tests

```
python -m pytest test_tsp.py test_main.py -v
```

`test_tsp.py` verifies the routing algorithm (Held-Karp) against brute-force search across all supported modes. `test_main.py` exercises the API's input validation and success path directly.

## Project structure

- `main.py` — FastAPI app, request validation
- `tsp.py` — exact TSP solver (Held-Karp) and route distance calculation
- `osrm.py` — real driving-duration matrix via the OSRM routing API
- `haversine.py` — straight-line distance utilities (not used by the live `/optimize` route; kept standalone)
- `page.html` — frontend: map, stop list, results, Google Maps handoff
- `test_tsp.py`, `test_main.py` — test suite
