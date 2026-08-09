"""
Checks for the Held-Karp solver.

The key test is agreement with brute force: brute force is obviously correct
(it tries every permutation), so matching it on random inputs is strong
evidence the DP is right.
"""

import itertools
import random

from tsp import held_karp, route_distance


def brute_force(dist, round_trip=True):
    n = len(dist)
    best, best_route = float("inf"), None
    for perm in itertools.permutations(range(1, n)):
        route = [0] + list(perm)
        cost = route_distance(dist, route, round_trip=round_trip)
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
    for n in range(2, 8):
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


if __name__ == "__main__":
    test_known_instance()
    test_matches_brute_force()
    test_edge_cases()
    test_asymmetric_costs()
    print("All tests passed.")