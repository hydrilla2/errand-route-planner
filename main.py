from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from osrm import get_duration_matrix
from tsp import held_karp, route_distance

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

"""when someone visit the root
    the read_root will be called
"""
@app.get("/") #the / is our root directory
def read_root():
    return {"Product": "Errand-Route-Planner",
            "version": "0.1.0",
            }

class Stop(BaseModel):
    name: str
    lat: float
    lng: float

class OptimizeRequest(BaseModel):
    stops: list[Stop]
    round_trip: bool = True
    end_index: int | None = None

@app.post("/optimize")
def optimize(req: OptimizeRequest):
    n = len(req.stops)
    if n <= 1 or n > 10:
        raise HTTPException(400, "Add between 2 and 10 stops.")

    if req.end_index is not None:
        if req.round_trip:
            raise HTTPException(400, "end_index cannot be used with round_trip.")
        if not (0 < req.end_index < n):
            raise HTTPException(400, "end_index must point to a stop other than the start.")

    try:
        matrix_input = get_duration_matrix(req.stops)
    except RuntimeError as e:
        raise HTTPException(502, f"Routing service error: {e}")

    best_cost, path = held_karp(matrix_input, req.round_trip, req.end_index)

    naive_end = None if req.round_trip else req.end_index
    naive_order = [i for i in range(n) if i != naive_end] + [naive_end] if naive_end is not None else list(range(n))
    naive_cost = route_distance(matrix_input, naive_order, req.round_trip)

    return {
        "order": path,
        "optimisedDistance": round(best_cost, 2),
        "naiveDistance": round(naive_cost, 2),
        "roundTrip": req.round_trip,
        "distanceSource": "osrm_duration_minutes",
    }

