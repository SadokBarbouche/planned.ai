from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings

embeddings = SentenceTransformerEmbeddings()

db = Chroma(persist_directory="../documentations", embedding_function=embeddings)


def fetch_best_plan(query, db=db):
    docs = db.similarity_search(query, k=2)
    return [doc.content for doc in docs]
