from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores.chroma import Chroma
from rag import load, split_texts
import os
import pandas as pd

if __name__ == "__main__":
    directory = "finetuning/it_datasets/qa_dataset/"
    embeddings = SentenceTransformerEmbeddings()

    for filename in os.listdir(directory):
        if filename.endswith(".xlsx"):
            if filename.startswith("concatenated"):
                continue
            each_place_df = pd.read_excel(directory + filename)
            each_place_df = each_place_df[['city', 'coordinates', 'instruction']]
            each_place_loader = load(each_place_df)
            each_place_docs = split_texts(each_place_df, each_place_loader)
            db_name = filename.replace(".xlsx", "")
            each_place_dir = os.path.join("db", db_name)
            os.mkdir(each_place_dir)
            each_place_db = Chroma.from_documents(
                each_place_docs,
                embedding=embeddings,
                persist_directory=each_place_dir
            )
