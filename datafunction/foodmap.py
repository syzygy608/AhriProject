import requests
import json

def get_resturants():
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];
    node(around:1200.00,23.557038,120.471707)["amenity"="restaurant"];

    out body;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    restaurants = []
    for r in data['elements']:
        restaurants.append(r['tags']['name'])
    return restaurants

print(get_resturants())

# node(around:800.00,23.557038,120.471707)["amenity"="restaurant"];
#
# out body;
# /*23.5530, 120.4760 23.5596, 120.4685    23.557038, 120.471707*/
