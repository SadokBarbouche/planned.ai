from rag import get_best_destination, pad_instruction
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
    instruction = pad_instruction("Staying in a hotel in el kef el kef el kef el kefcity ", 1430)
    print(get_best_destination(db=db, user_input=instruction))