from langchain_community.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd


def pad_instruction(instruction: str, max_length: int):
    padding_length = max_length - len(instruction)
    padded_instruction = instruction + ' ' * padding_length
    return padded_instruction


def load(df: pd.DataFrame):
    loader = DataFrameLoader(df, page_content_column="instruction")
    return loader


def split_texts(df: pd.DataFrame, loader: DataFrameLoader):
    df['instruction'] = df['instruction'].astype(str)
    # Having the same size for all the chunks
    chunk_size = int(df['instruction'].apply(len).max())
    df['instruction'] = df['instruction'].apply(pad_instruction, args=(chunk_size,))
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=10,
        length_function=len,
    )
    texts = splitter.split_documents(loader.load())
    # print(texts)
    return texts


def get_best_destination(user_input: str, db):
    docs = db.similarity_search(user_input, k=5)
    return docs
