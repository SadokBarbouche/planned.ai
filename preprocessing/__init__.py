from city_names import extract_city_name
from geolocation import get_location
import pandas as pd

if __name__ == "__main__":
    data = pd.read_excel("concatenated_output.xlsx")

    data['coordinates'] = data['address'].apply(get_location)
    data['latitude'] = data['coordinates'].apply(lambda x: x[0] if x is not None else None)
    data['longitude'] = data['coordinates'].apply(lambda x: x[1] if x is not None else None)
    data.to_excel("Data with geolocation.xlsx")

    city_names = pd.read_json("../data/output/tunisia-cities.json")
    df = pd.read_excel("Data with geolocation.xlsx")
    df['city'] = df['address'].apply(extract_city_name)
    df.to_excel("Data with city names.xlsx")
