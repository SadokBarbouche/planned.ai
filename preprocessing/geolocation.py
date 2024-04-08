import pandas as pd
import requests


def get_location(address):
    url = f"https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?f=json&SingleLine={address}"
    response = requests.get(url)
    data = response.json()
    if 'candidates' in data and len(data['candidates']) > 0:
        lat = data['candidates'][0]['location']['y']
        lng = data['candidates'][0]['location']['x']
        return lat, lng
    else:
        return None


data = pd.read_excel("concatenated_output.xlsx")
data['coordinates'] = data['address'].apply(get_location)
data['latitude'] = data['coordinates'].apply(lambda x: x[0] if x is not None else None)
data['longitude'] = data['coordinates'].apply(lambda x: x[1] if x is not None else None)

data.to_excel("Data with geolocation.xlsx")
