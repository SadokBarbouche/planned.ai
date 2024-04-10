import os
import pandas as pd


def concat_dataframes(directory):
    dfs = []
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx"):
            filepath = os.path.join(directory, filename)
            df = pd.read_excel(filepath)
            dfs.append(df)

    concatenated_df = pd.concat(dfs, ignore_index=True)
    concatenated_df.to_excel(directory+'/concatenated_dfs.xlsx')

    return concatenated_df


if __name__ == "__main__":
    it_directory_path = '../finetuning/it_datasets/it_dataset'
    qa_directory_path = '../finetuning/it_datasets/qa_dataset'
    it_datasets_concat = concat_dataframes(it_directory_path)
    qa_it_datasets_concat = concat_dataframes(qa_directory_path)

