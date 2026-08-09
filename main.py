from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from haversine import matrix_convertor 
from tsp import held_karp

app = FastAPI()

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
    if len(req.stops) <= 0 or len(req.stops) >= 10:
        raise HTTPException(400, "Add between 2 and 10 stops.")
    matrix_input = matrix_convertor(req.stops)
    best_cost, path = held_karp(matrix_input)

    return {
    "order": path,
    "optimisedDistance": round(best_cost, 2),
    "naiveDistance": round(naive_cost, 2),
    "roundTrip": req.round_trip,
    } 


