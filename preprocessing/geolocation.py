import requests


def get_location(address):
    """
    Retrieves latitude and longitude coordinates for a given address using the ArcGIS geocoding service.
    Args:
        address (str): The address for which to retrieve location coordinates.
    Returns:
        tuple or None: A tuple containing latitude and longitude coordinates (lat, lng) if the address is found,
                       otherwise returns None.
    Note:
        This function sends a request to the ArcGIS geocoding service and parses the response to extract
        latitude and longitude coordinates for the provided address. If the address is not found, it returns None.
    """
    url = f"https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?f=json&SingleLine={address}"
    response = requests.get(url)
    data = response.json()
    if 'candidates' in data and len(data['candidates']) > 0:
        lat = data['candidates'][0]['location']['y']
        lng = data['candidates'][0]['location']['x']
        return lat, lng
    else:
        return None


