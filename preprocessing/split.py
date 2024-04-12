import pandas as pd


def split(df: pd.DataFrame) -> None:
    """
    Splits a DataFrame into multiple Excel files based on unique city names.
    Args:
        df (pandas.DataFrame): The DataFrame to be split.
    Returns:
        None
    Note:
    - This function extracts unique city names from the 'city' column of the DataFrame.
    - It iterates through each unique city and creates a subset of db for that city.
    - Each subset of db is saved to an Excel file named '{city}_dataset.xlsx' in the 'cities' directory.
    """
    unique_cities = df['city'].unique()
    for city in unique_cities:
        city_data = df[df['city'] == city]
        filename = f'../data/cities/{city}_dataset.xlsx'
        city_data.to_excel(filename, index=False)
