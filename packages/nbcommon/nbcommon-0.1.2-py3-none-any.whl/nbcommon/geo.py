import math
import json


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

def to_poly_filter(gjson: str, name:str='default'):
    loaded = json.loads(gjson)
    if len(loaded['features']) > 1:
        raise ValueError('multiple features geojson is not supported')
    geometry = loaded['features'][0]['geometry']
    if geometry['type'] != 'Polygon':
        raise ValueError('only converting from geojson polygon is supported')
    if len(geometry['coordinates']) > 1:
        logging.warn('multiple coordinates of polygon detected, only using first one as exterior definition')
    output = [name,'area1']
    for coord in geometry['coordinates'][0]:
        output.append(f'\t{coord[0]}\t{coord[1]}')
    output.append('END')
    output.append('END')
    return '\n'.join(output)

def poly_to_geojson(poly: str):
    gjson = {
        'type': 'FeatureCollection',
        'name': 'default',
        'features': [
            {
                'type': 'Feature',
                'properties': {},
                'geometry':{
                    'type': 'Polygon',
                    'coordinates': [
                        []
                    ]
                }
            }
        ]
    }
    lines = poly.split('\n')
    gjson['name'] = lines[0].strip()
    for line in lines[2:len(lines)-2]:
        coords = line.strip().split('\t') 
        gjson['features'][0]['geometry']['coordinates'][0].append([float(coords[0]),float(coords[1])])
    return gjson
