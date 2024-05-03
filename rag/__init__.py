# from rag import get_best_destination, pad_instruction
# from langchain.vectorstores.chroma import Chroma
# from langchain_community.embeddings import SentenceTransformerEmbeddings
# from langchain.embeddings import CacheBackedEmbeddings
# from langchain.storage import LocalFileStore
# if __name__ == "__main__":
#     fs = LocalFileStore("./cache/")
#     embeddings = SentenceTransformerEmbeddings()
#     cached_embedder = CacheBackedEmbeddings.from_bytes_store(
#         embeddings, fs, namespace="sentence-transformer"
#     )
#     db = Chroma(
#         persist_directory="db/qa_it_ariana_dataset/",
#         embedding_function=embeddings
#     )
    
#     instruction ="I want to spend the night in a nightclub in ariana"
#     print(get_best_destination(db=db, user_input=instruction))