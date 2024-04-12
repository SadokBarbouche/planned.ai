from langchain_community.document_loaders import DataFrameLoader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from chroma import fetch_best_plan, embeddings
import pandas as pd

df = pd.read_excel('')
loader = DataFrameLoader(df, page_content_column="Team")
docs = []
db = Chroma.from_documents(
    docs,
    embedding=embeddings,
    persist_directory="../documentations"
)

if __name__ == "__main__":
    test_query = ""
    print(fetch_best_plan(query=test_query))
