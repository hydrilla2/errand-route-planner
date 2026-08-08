import math
from tcp import held_karp

def haversine(lat1 ,long1 ,lat2 ,long2 ):
    Radius = 6371.0088

    # Convert degrees to radians
    lat1, long1, lat2, long2 = map(math.radians, [lat1, long1, lat2, long2])

    dlat = lat2 - lat1
    dlon = long2 - long1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return Radius * c

d = haversine(3.1390, 101.6869, 2.1896, 102.2501)
print(f"{d:.2f} km")

"""
convert distance between two stops into matrix
lyon = (45.7597, 4.8422) # (lat, lon)
paris = (48.8567, 2.3508)
kuala lumpur = (3.1412, 101.6865)
"""

stops = [(45.7597, 4.8422), (48.8567, 2.3508),(3.1412, 101.6865)]

def matrix_convertor(stops):
    """
     dist = [
        [0, 1, 9],
        [9, 0, 1],
        [1, 9, 0],
    ]
    """
    n_stops = len(stops)

    if n_stops == 0 or n_stops == 1:
        return [[0]]
    matrix_dis = [[0] * n_stops for _ in range(n_stops) ]

    for i in range(n_stops):
        for j in range(n_stops):

            if i == j:
                continue

            distance = haversine(stops[i][0],stops[i][1],stops[j][0],stops[j][1])
            #print(stops[i][0],stops[i][1],stops[j][0],stops[j][1])
            matrix_dis[i][j] = distance

    return matrix_dis

dist = matrix_convertor(stops)
bestcost, route = held_karp(dist)
print(f"best cost {bestcost}\n")
print(f"route: {route}")