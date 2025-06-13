import os
import pickle
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.docstore.document import Document
from llm.response_engine import rerank_documents

class HybridRetriever:
    def __init__(self, top_k=8):
        self.top_k = top_k

        # Load Hugging Face embedding model
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # === Load FAISS vector store ===
        with open("vector_store/faiss_store.pkl", "rb") as f:
            self.dense_vectorstore = pickle.load(f)
        dense_retriever = self.dense_vectorstore.as_retriever(search_kwargs={"k": top_k})

        # === Load BM25 sparse retriever ===
        with open("vector_store/bm25_corpus.pkl", "rb") as f:
            bm25_docs = pickle.load(f)
        sparse_retriever = BM25Retriever.from_documents(bm25_docs)
        sparse_retriever.k = top_k

        # === Combine with EnsembleRetriever ===
        self.hybrid_retriever = EnsembleRetriever(
            retrievers=[dense_retriever, sparse_retriever],
            weights=[0.5, 0.5]  # equal score fusion weight
        )

    def get_relevant_documents(self, query: str):
        retrieved_docs = self.hybrid_retriever.get_relevant_documents(query)

        # Optional: Re-rank with LLM
        reranked = rerank_documents(query, retrieved_docs)
        return reranked[:self.top_k]
