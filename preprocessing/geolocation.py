from geopy.geocoders import Nominatim
import pandas as pd

df = pd.read_excel("concatenated_output.xlsx")

loc = Nominatim(user_agent="GetLoc")

df["Localisation"] = ""
for i in range(len(df)):
    try:
        getLoc = loc.geocode(df["address"][i])
        print(getLoc.address)
        # print("Latitude = ", getLoc.latitude, "\n")
        # print("Longitude = ", getLoc.longitude)
        df["Localisation"][i] = getLoc.address
    except:
        print("Error")
