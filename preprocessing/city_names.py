def extract_city_name(address, city_names=city_names):
    """
    Extracts the city name from an address based on a predefined list of city names.

    Args:
        address (str): The address from which to extract the city name.
        city_names (pandas.DataFrame): A DataFrame containing a list of city names.

    Returns:
        str: The extracted city name if found in the address, otherwise returns "City Not Found".

    Note:
    - This function converts the address to lowercase for case-insensitive comparison.
    - It iterates through the list of city names and checks if each city name is present in the address.
    - If a city name is found in the address, it returns the city name. Otherwise, it returns "City Not Found".
    """
    address_lower = str(address).lower()
    for city in city_names.loc[:, 0]:
        if city.lower() in address_lower:
            return city
    return "City Not Found"
