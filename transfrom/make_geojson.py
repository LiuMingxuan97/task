from geojson import Point, Feature, FeatureCollection
import json


points = [
    {"name": "scan1 1", "coordinates": [-76.42343496, -41.77437925, ]},
    {"name": "scan1 2", "coordinates": [-76.64857326, -41.81455339, ]},
    {"name": "scan1 3", "coordinates": [-76.86820047, -41.85337898, ]},
    {"name": "scan2 1", "coordinates": [-76.44635353, -41.70732563, ]},
    {"name": "scan2 2", "coordinates": [-76.67125228, -41.74746274, ]},
    {"name": "scan2 3", "coordinates": [-76.89064558, -41.78625335, ]},
    {"name": "scan3 1", "coordinates": [-76.4688726,  -41.64025592, ]},
    {"name": "scan3 2", "coordinates": [-76.69354882, -41.68034247, ]},
    {"name": "scan3 3", "coordinates": [-76.91272353, -41.71908466, ]},
]

features = []
for point in points:
    features.append(
        Feature(
            geometry=Point(point['coordinates']),
            properties={"name": point['name']}
        )
    )

feature_collection = FeatureCollection(features)




with open(r'D:\code\pycode\task\transfrom\img.geojson', 'w') as f:
    json.dump(feature_collection, f)