import math


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