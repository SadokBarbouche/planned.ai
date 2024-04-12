from rag import get_best_destination
from langchain.vectorstores.chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
if __name__ == "__main__":
    fs = LocalFileStore("./cache/")
    embeddings = SentenceTransformerEmbeddings()
    cached_embedder = CacheBackedEmbeddings.from_bytes_store(
        embeddings, fs, namespace="sentence-transformer"
    )
    db = Chroma(
        persist_directory="db",
        embedding_function=embeddings
    )
    print(get_best_destination(db=db, user_input='I want to visit El Kef and visit natural places.'))
