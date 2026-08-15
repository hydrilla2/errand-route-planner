def held_karp(dist, round_trip = True, end_index = None):

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

    if round_trip:
            best_cost = float('inf')
            best_last = -1
            for j in range(n):
                if j == 0:
                    continue
                cost = dp[FULL][j] + dist[j][0]
                if cost < best_cost:
                    best_cost = cost
                    best_last = j
    elif end_index is not None:
        best_last = end_index
        best_cost = dp[FULL][best_last]
    else:
        best_cost = float('inf')
        best_last = -1
        for j in range(n):
            if j == 0:
                continue
            cost = dp[FULL][j]
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

def route_distance(matrix, order, round_trip=True):
    total = 0
    if len(order) == 0 or len(order) == 1:
        return 0

     
    for i in range(len(order) - 1):

        total += matrix[order[i]][order[i+1]]

    if round_trip:
        total += matrix[order[len(order)-1]][0]

    # walk consecutive pairs in `order`, adding matrix[from][to] each time
    # then, if round_trip, add the leg from the last stop back to the first
    return total

if __name__ == "__main__":
    testing1 = held_karp([[]])

    cost, path = testing1
    print(f"cost {cost}, path: {path}")