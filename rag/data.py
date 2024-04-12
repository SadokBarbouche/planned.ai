import pandas as pd
import os


def prepare(data_directory='../finetuning/it_datasets/qa_dataset', rag_data_path='./data'):
    for dataset in os.listdir(data_directory):
        if f"rag_{dataset}" in os.listdir(rag_data_path):
            print(f"{dataset} already processed")
            continue

        if dataset.endswith('.xlsx') or dataset.endswith('.xls'):
            try:
                df = pd.read_excel(f'{data_directory}/{dataset}', usecols=['choices', 'plan', 'coordinates'])
                # df['index'] = range(len(df))
                df = df[df['plan'] != "" or df['choices'] != "" or df['coordinates'] != ""]
                df.to_excel(f"{rag_data_path}/rag_{dataset}")
            except Exception as e:
                print(f"Error with dataset : {dataset}")
                continue
