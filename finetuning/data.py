import pandas as pd
import os


def prepare(data_directory='../finetuning/it_datasets/qa_dataset', ft_data_path='finetuning_data'):
    for dataset in os.listdir(data_directory):
        if f"rag_{dataset}" in os.listdir(ft_data_path):
            print(f"{dataset} already processed")
            continue

        if dataset.endswith('.xlsx') or dataset.endswith('.xls'):
            try:
                df = pd.read_excel(f'{data_directory}/{dataset}', usecols=['choices', 'plan', 'coordinates'])
                # df['index'] = range(len(df))
                df = df[(df['plan'] != "") | (df['choices'] != "") | (df['coordinates'] != "")]
                df.to_excel(f"{rag_data_path}/rag_{dataset}")
            except Exception as e:
                print(f"Error with dataset : {dataset}")
                continue


def format_data(ft_data_path='finetuning_data'):
    for dataset in os.listdir(ft_data_path):
        df = pd.read_excel(f'{ft_data_path}/{dataset}')
        for i in range(len(df)):
            df['choices'][i] = df['choices'][i].replace("*", "")
            df['choices'][i] = df['choices'][i].replace("\n\n", "\n")
            df['plan'][i] = df['plan'][i].replace("*", "")
            df['plan'][i] = df['plan'][i].replace("\n\n", "\n")
        df.to_excel(f'{ft_data_path}/{dataset}', index=False)




def rename(ft_data_path='finetuning_data'):
    for dataset in os.listdir(ft_data_path):
        os.rename(f'{ft_data_path}/{dataset}', ''.join(list(dataset)[4:]))


def drop(ft_data_path='finetuning_data'):
    for dataset in os.listdir(ft_data_path):
        df = pd.read_excel(f'{ft_data_path}/{dataset}')
        df.drop(columns=['coordinates'], inplace=True)
        df.to_excel(f'{ft_data_path}/{dataset}', index=False)


def concat_dataframes(directory='finetuning_data'):
    dfs = []
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx"):
            filepath = os.path.join(directory, filename)
            df = pd.read_excel(filepath)
            dfs.append(df)

    concatenated_df = pd.concat(dfs, ignore_index=True)
    concatenated_df.to_excel(directory + '/concatenated_dfs.xlsx')

    return concatenated_df
