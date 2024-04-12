from typing import Optional, List, Dict, Any

from langchain.embeddings.base import Embeddings
from langchain.vectorstores.chroma import Chroma
from langchain.schema import BaseRetriever
from langchain_core.callbacks import Callbacks
from langchain_core.documents import Document


class RedundantFilterRetriever(BaseRetriever):
    embeddings: Embeddings
    chroma: Chroma

    def _get_relevant_documents(
            self,
            query: str,
            *,
            callbacks: Callbacks = None,
            tags: Optional[List[str]] = None,
            metadata: Optional[Dict[str, Any]] = None,
            run_name: Optional[str] = None,
            **kwargs: Any,
    ) -> List[Document]:
        emb = self.embeddings.embed_query(query)
        return self.chroma.max_marginal_relevance_search_by_vector(
            embedding=emb,
            lambda_mult=0.8
        )

    def _aget_relevant_documents(
            self,
            query: str,
            *,
            callbacks: Callbacks = None,
            tags: Optional[List[str]] = None,
            metadata: Optional[Dict[str, Any]] = None,
            run_name: Optional[str] = None,
            **kwargs: Any,
    ) -> List[Document]:
        return []
