import requests
import json

def get_resturants(): # type: list
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
        info = {'name':r['tags']['name'], # node name
                'link': "https://www.openstreetmap.org/node/" + str(r['id']) #node link
               }
        restaurants.append(info)
    return restaurants # restaurants['name']:餐廳名稱, restaurants['link']: 位置連結

R = get_resturants()
print(R)
print(R[2]['name'], R[2]['link'])

# node(around:800.00,23.557038,120.471707)["amenity"="restaurant"];
#
# out body;
# /*23.5530, 120.4760 23.5596, 120.4685    23.557038, 120.471707*/
