import pandas as pd
df = pd.read_excel('preprocessed_data/Data with city names.xlsx')
unique_cities = df['city'].unique()
for city in unique_cities:
    city_data = df[df['city'] == city]
    filename = f'../data/cities/{city}_dataset.xlsx'
    city_data.to_excel(filename, index=False)
