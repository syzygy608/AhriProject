import overpass
api = overpass.API()
response = api.get('node["name"="中正大學"]')
print(response)
