"""
Checks for the Held-Karp solver.

The key test is agreement with brute force: brute force is obviously correct
(it tries every permutation), so matching it on random inputs is strong
evidence the DP is right.
"""
import time
import itertools
import random
from haversine import matrix_convertor, Point

from tsp import held_karp, route_distance


def brute_force(dist, round_trip=True):
    n = len(dist)
    best, best_route = float("inf"), None

    if round_trip:
        candidates = range(1, n)
        for perm in itertools.permutations(candidates):
            route = [0] + list(perm)
            cost = route_distance(dist, route, round_trip=True)
            if cost < best:
                best, best_route = cost, route
    else:
        middle = [i for i in range(1, n) if i != n - 1]
        for perm in itertools.permutations(middle):
            route = [0] + list(perm) + [n - 1]
            cost = route_distance(dist, route, round_trip=False)
            if cost < best:
                best, best_route = cost, route

    return best, best_route


def test_known_instance():
    """Classic 4-city instance with a known optimal tour of 80."""
    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]
    cost, order = held_karp(dist)
    assert cost == 80, cost
    assert order[0] == 0


def test_matches_brute_force():
    """Random instances, both round trip and one way."""
    random.seed(1)
    for n in range(2, 11):
        for round_trip in (True, False):
            dist = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if i != j:
                        dist[i][j] = random.randint(1, 50)
            hk_cost, hk_order = held_karp(dist, round_trip=round_trip)
            bf_cost, _ = brute_force(dist, round_trip=round_trip)
            assert abs(hk_cost - bf_cost) < 1e-9, (n, round_trip, hk_cost, bf_cost)
            # the returned order must be a genuine permutation of every stop
            assert sorted(hk_order) == list(range(n)), hk_order
            # and its cost must match what was reported
            assert abs(route_distance(dist, hk_order, round_trip) - hk_cost) < 1e-9


def test_edge_cases():
    assert held_karp([]) == (0.0, [])
    assert held_karp([[0]]) == (0.0, [0])
    cost, order = held_karp([[0, 7], [7, 0]])
    assert cost == 14 and order == [0, 1]      # round trip: out and back
    cost, order = held_karp([[0, 7], [7, 0]], round_trip=False)
    assert cost == 7 and order == [0, 1]


def test_asymmetric_costs():
    """Road distances are not always symmetric (one-way streets)."""
    dist = [
        [0, 1, 9],
        [9, 0, 1],
        [1, 9, 0],
    ]
    cost, order = held_karp(dist)
    assert order == [0, 1, 2] and cost == 3, (order, cost)

import time

def test_performance_n10():
    """Held-Karp should stay fast at the API's max stop count."""
    random.seed(2)
    n = 10
    dist = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = random.randint(1, 50)

    start = time.perf_counter()
    held_karp(dist)
    elapsed = time.perf_counter() - start

    assert elapsed < 1.0, f"Held-Karp took {elapsed:.3f}s at n=10 — investigate"

# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_rejects_too_few_stops():
    res = client.post("/optimize", json={"stops": [{"name": "A", "lat": 0, "lng": 0}]})
    assert res.status_code == 400

def test_rejects_too_many_stops():
    stops = [{"name": str(i), "lat": i, "lng": i} for i in range(11)]
    res = client.post("/optimize", json={"stops": stops, "round_trip": True})
    assert res.status_code == 400

def test_valid_request_returns_200():
    stops = [
        {"name": "A", "lat": 3.1073, "lng": 101.6067},
        {"name": "B", "lat": 3.1177, "lng": 101.6770},
        {"name": "C", "lat": 3.1578, "lng": 101.7118},
    ]
    res = client.post("/optimize", json={"stops": stops, "round_trip": True})
    assert res.status_code == 200
    data = res.json()
    assert sorted(data["order"]) == [0, 1, 2]
    assert data["optimisedDistance"] <= data["naiveDistance"] + 1e-9

if __name__ == "__main__":
    test_known_instance()
    test_matches_brute_force()
    test_edge_cases()
    test_asymmetric_costs()
    test_performance_n10()
    test_rejects_too_few_stops()
    test_rejects_too_many_stops()
    test_valid_request_returns_200()
    print("All tests passed.")