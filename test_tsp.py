"""
Checks for the Held-Karp solver.

Held-Karp now supports three modes:
  - round_trip=True                      -> loop back to stop 0
  - round_trip=False, end_index=None     -> end anywhere (free choice)
  - round_trip=False, end_index=k        -> end fixed at stop k

The key test is agreement with brute force: brute force is obviously correct
(it tries every permutation under the same constraint), so matching it on
random inputs is strong evidence the DP is right for all three modes.
"""

import itertools
import random

from tsp import held_karp, route_distance


def brute_force(dist, round_trip=True, end_index=None):
    n = len(dist)
    best, best_route = float("inf"), None

    if round_trip:
        for perm in itertools.permutations(range(1, n)):
            route = [0] + list(perm)
            cost = route_distance(dist, route, round_trip=True)
            if cost < best:
                best, best_route = cost, route

    elif end_index is not None:
        middle = [i for i in range(1, n) if i != end_index]
        for perm in itertools.permutations(middle):
            route = [0] + list(perm) + [end_index]
            cost = route_distance(dist, route, round_trip=False)
            if cost < best:
                best, best_route = cost, route

    else:
        for perm in itertools.permutations(range(1, n)):
            route = [0] + list(perm)
            cost = route_distance(dist, route, round_trip=False)
            if cost < best:
                best, best_route = cost, route

    return best, best_route


def random_matrix(n, seed):
    random.seed(seed)
    dist = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = random.randint(1, 50)
    return dist


def test_matches_brute_force():
    """Random instances, n=2-7, round-trip and free-destination modes."""
    for n in range(2, 8):
        for round_trip in (True, False):
            dist = random_matrix(n, seed=n * 10 + round_trip)

            hk_cost, hk_order = held_karp(dist, round_trip=round_trip)
            bf_cost, _ = brute_force(dist, round_trip=round_trip)

            assert abs(hk_cost - bf_cost) < 1e-9, (n, round_trip, hk_cost, bf_cost)

            # the returned order must be a genuine permutation of every stop
            assert sorted(hk_order) == list(range(n)), hk_order

            # and its cost must match what route_distance independently computes
            recomputed = route_distance(dist, hk_order, round_trip)
            assert abs(recomputed - hk_cost) < 1e-9, (recomputed, hk_cost)


def test_matches_brute_force_fixed_destination():
    """Random instances, n=2-7, every valid fixed end_index."""
    for n in range(2, 8):
        dist = random_matrix(n, seed=1000 + n)

        for end_index in range(1, n):
            hk_cost, hk_order = held_karp(dist, round_trip=False, end_index=end_index)
            bf_cost, _ = brute_force(dist, round_trip=False, end_index=end_index)

            assert abs(hk_cost - bf_cost) < 1e-9, (n, end_index, hk_cost, bf_cost)
            assert sorted(hk_order) == list(range(n)), hk_order
            assert hk_order[-1] == end_index, hk_order  # destination must be fixed

            recomputed = route_distance(dist, hk_order, round_trip=False)
            assert abs(recomputed - hk_cost) < 1e-9, (recomputed, hk_cost)


def test_edge_cases():
    assert held_karp([]) == (0.0, [])
    assert held_karp([[0]]) == (0.0, [0])

    cost, order = held_karp([[0, 7], [7, 0]])
    assert cost == 14 and order == [0, 1]  # round trip: out and back

    cost, order = held_karp([[0, 7], [7, 0]], round_trip=False)
    assert cost == 7 and order == [0, 1]  # free destination, only one option

    cost, order = held_karp([[0, 7], [7, 0]], round_trip=False, end_index=1)
    assert cost == 7 and order == [0, 1]  # fixed destination, same result here


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
    test_matches_brute_force()
    test_matches_brute_force_fixed_destination()
    test_edge_cases()
    test_asymmetric_costs()
    print("All tests passed.")
