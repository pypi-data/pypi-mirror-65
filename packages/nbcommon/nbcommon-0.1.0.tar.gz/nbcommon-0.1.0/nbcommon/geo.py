import math


class LatLng:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

def distance(loc1: LatLng, loc2: LatLng):
    # approximate radius of earth in meter
    R = 6373000

    lat1 = math.radians(loc1.lat)
    lng1 = math.radians(loc1.lng)
    lat2 = math.radians(loc2.lat)
    lng2 = math.radians(loc2.lng)

    dlng = lng2 - lng1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlng / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
