import pandas as pd

city_names = pd.read_json("../data/output/tunisia-cities.json")
df = pd.read_excel("Data with geolocation.xlsx")


def extract_city_name(address, city_names=city_names):
    address_lower = str(address).lower()
    for city in city_names.loc[:, 0]:
        if city.lower() in address_lower:
            return city
    return "City Not Found"


df['city'] = df['address'].apply(extract_city_name)
df.to_excel("Data with city names.xlsx")
