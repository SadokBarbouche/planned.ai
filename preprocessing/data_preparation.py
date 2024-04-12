import os
import json
import pandas as pd


def no_empty_columns(df: pd.DataFrame) -> list:
    """
       Finds columns in a DataFrame that do not contain any empty (NaN) values.

       Args:
           df (pd.DataFrame): The DataFrame to analyze.

       Returns:
           list: A list containing the names of columns with no empty values.

       Note:
           This function iterates through each column of the DataFrame and checks if there are any empty values
           (NaN). Columns with no empty values are added to the list and returned.
    """
    no_empty_cols = []
    for col in df.columns:
        if not df[col].isnull().any():
            no_empty_cols.append(col)
    return no_empty_cols


def concat_json_files(directory):
    """
    Concatenates JSON files found within a directory and its subdirectories.

    Args:
        directory (str): The path to the directory containing JSON files.

    Returns:
        list: A list containing the combined db from all JSON files.

    Note:
        This function recursively searches through the specified directory and its subdirectories
        for JSON files. It reads each JSON file, extracts its db, and appends it to the output list.
        If a JSON file cannot be read due to a JSONDecodeError, it prints an error message and continues
        to the next file.
    """
    output_data = []
    for root, dirs, files in os.walk(directory):
        if 'json' in dirs:
            json_folder_path = os.path.join(root, 'json')
            for json_root, _, json_files in os.walk(json_folder_path):
                for file in json_files:
                    if file.endswith('.json'):
                        file_path = os.path.join(json_root, file)
                        with open(file_path, 'r') as f:
                            try:
                                data = json.load(f)
                                output_data.extend(data)
                            except json.JSONDecodeError:
                                print(f"Error reading JSON file: {file_path}")
                                continue

    return output_data


def main():
    """
    Main function to concatenate JSON files, convert the combined db to a DataFrame,
    and write it to an Excel file.

    Note:
    - This function specifies the directory containing JSON files.
    - It calls the 'concat_json_files' function to concatenate JSON files within the directory.
    - The combined db is then converted to a DataFrame using pandas.
    - Finally, the DataFrame is saved to an Excel file named 'concatenated_output.xlsx'.
    """
    directory = '../db/output'
    output_data = concat_json_files(directory)
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(output_data)
    # Write DataFrame to Excel file
    df.to_excel("concatenated_output.xlsx", index=False)
    print("Concatenation completed. Result saved to 'concatenated_output.xlsx'")


if __name__ == "__main__":
    main()
