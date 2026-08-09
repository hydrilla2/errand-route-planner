def held_karp(dist):

    #dist is the distance between each locations
    n = len(dist)

    if n == 0:
        return 0.0, []

    elif n == 1:
        return 0.0, [0]
    
    FULL = (1 << n) - 1
    
    # dp[mask][j] = min cost to visit stops in `mask`, ending at j
    dp = [[float('inf')] * n for _ in range(1 << n)]

    #to record which stop we come from
    parent = [[-1] * n for _ in range(1 << n)]  # for backtracking the route
    
    dp[1][0] = 0  # only stop 0 visited, ending at 0

    #mask shows the status of each location (visited?)
    # 1 << 4 = 16
    for mask in range(1 << n):

        #j represents every possible current position
        for j in range(n):
            if not (mask & (1 << j)):
                continue  # j not in this subset
            if dp[mask][j] == float('inf'):
                continue  # unreachable state, skip

            #every possible "next stop to add"
            for k in range(n):
                if mask & (1 << k):
                    continue  # k already visited, can't go there
                new_mask = mask | (1 << k)
                new_cost = dp[mask][j] + dist[j][k]
                if new_cost < dp[new_mask][k]:
                    dp[new_mask][k] = new_cost
                    parent[new_mask][k] = j  # remember how we got here
    
    # find best end point
    #best_cost = min(dp[FULL][j] for j in range(1, n))  # or +dist[j][0] if round-trip

    best_cost = float('inf')
    best_last = -1

    for j in range(n):
        if j == 0:
            continue  # can't end at the start with nothing else visited, skip self-loop case
        cost = dp[FULL][j] + dist[j][0]   # + cost to return home
        if cost < best_cost:
            best_cost = cost
            best_last = j


    # TODO: backtrack using `parent` to reconstruct the actual route order
    path = []
    mask, j = FULL, best_last

    while j != -1:
        path.append(j)
        prev_j = parent[mask][j]     # look up predecessor BEFORE changing j
        mask = mask & ~(1 << j)      # remove the OLD j from mask (using old j, still available)
        j = prev_j
 
    path.reverse()


    return best_cost, path

if __name__ == "__main__":
    testing1 = held_karp([[]])

    cost, path = testing1
    print(f"cost {cost}, path: {path}")