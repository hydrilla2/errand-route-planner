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
    
@app.post("/optimize")
def optimize(req: OptimizeRequest):
    # 1. reject bad input (too few stops, too many for Held-Karp)
    if len(req.stops) <= 1 or len(req.stops) > 10:
        raise HTTPException(400, "Add between 2 and 10 stops.")
    try:
        matrix_input = get_duration_matrix(req.stops)
    except RuntimeError as e:
        raise HTTPException(502, f"Routing service error: {e}")
    best_cost, path = held_karp(matrix_input, req.round_trip)
    naive_cost = route_distance(matrix_input, list(range(len(req.stops))), req.round_trip)

    return {
    "order": path,
    "optimisedDistance": round(best_cost, 2),
    "naiveDistance": round(naive_cost, 2),
    "roundTrip": req.round_trip,
    "distanceSource": "osrm_duration_minutes",
    } 


