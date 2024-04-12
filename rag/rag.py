from langchain_community.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd


def load(df: pd.DataFrame):
    loader = DataFrameLoader(df, page_content_column="instruction")
    return loader


def split_texts(df: pd.DataFrame, loader: DataFrameLoader):
    df['instruction'] = df['instruction'].astype(str)
    chunk_size = int(df['instruction'].apply(len).mean())
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=100,
        length_function=len,
    )
    texts = splitter.split_documents(loader.load())
    # print(texts)
    return texts


def get_best_destination(user_input: str, db):
    docs = db.similarity_search(user_input, k=2)
    return docs

