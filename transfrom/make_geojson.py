from geojson import Point, Feature, FeatureCollection
import json


points = [
    {"name": "Point 1", "coordinates": [-41.816042930779226, -76.13657011871047]},
    {"name": "Point 2", "coordinates": [-41.82635276112756, -76.19398064484739]},
    {"name": "Point 3", "coordinates": [-41.8365725688295, -76.25102610506781]},
    {"name": "Point 3", "coordinates": [-41.84670367369686, -76.30771122331782]},
    {"name": "Point 3", "coordinates": [-41.85674736775437, -76.36404063093751]},
    {"name": "Point 3", "coordinates": [-41.86670491600722, -76.42001886910552]},
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




with open('point.geojson', 'w') as f:
    json.dump(feature_collection, f)