def held_karp(dist):

    #dist is the distance between each locations
    n = len(dist)
    FULL = (1 << n) - 1
    
    # dp[mask][j] = min cost to visit stops in `mask`, ending at j
    dp = [[float('inf')] * n for _ in range(1 << n)]

    #to record which stop we come from
    parent = [[-1] * n for _ in range(1 << n)]  # for backtracking the route
    
    dp[1][0] = 0  # only stop 0 visited, ending at 0
    
    for mask in range(1 << n):
        for j in range(n):
            if not (mask & (1 << j)):
                continue  # j not in this subset
            if dp[mask][j] == float('inf'):
                continue  # unreachable state, skip
            for k in range(n):
                if mask & (1 << k):
                    continue  # k already visited, can't go there
                new_mask = mask | (1 << k)
                new_cost = dp[mask][j] + dist[j][k]
                if new_cost < dp[new_mask][k]:
                    dp[new_mask][k] = new_cost
                    parent[new_mask][k] = j  # remember how we got here
    
    # find best end point
    best_cost = min(dp[FULL][j] for j in range(1, n))  # or +dist[j][0] if round-trip
    # TODO: backtrack using `parent` to reconstruct the actual route order
    
    return best_cost