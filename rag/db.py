from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores.chroma import Chroma
from redundant_fiter_retriever import RedundantFilterRetriever
from rag import load, split_texts
import pandas as pd

if __name__ == "__main__":
    df = pd.read_excel('../finetuning/it_datasets/qa_dataset/concatenated_dfs.xlsx')
    df = df[['city', 'coordinates', 'instruction']]

    loader = load(df)
    docs = split_texts(df, loader)

    embeddings = SentenceTransformerEmbeddings()

    db = Chroma.from_documents(
        docs,
        embedding=embeddings,
        persist_directory="db"
    )

    retriever = RedundantFilterRetriever(
        embeddings=embeddings,
        chroma=db
    )
