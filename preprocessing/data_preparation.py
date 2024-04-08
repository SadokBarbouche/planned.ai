import os
import json
import pandas as pd


def no_empty_columns(df: pd.DataFrame) -> list:
    no_empty_cols = []
    for col in df.columns:
        if not df[col].isnull().any():
            no_empty_cols.append(col)
    return no_empty_cols


def concat_json_files(directory):
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
    directory = '../data/output'
    output_data = concat_json_files(directory)
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(output_data)
    # Write DataFrame to Excel file
    df.to_excel("concatenated_output.xlsx", index=False)
    print("Concatenation completed. Result saved to 'concatenated_output.xlsx'")


if __name__ == "__main__":
    main()
