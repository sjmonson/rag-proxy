from rag_proxy.vectordb import VectorDB
from rag_proxy.embedding import Embedding

class RAG(object):
    def __init__(self, database: VectorDB, embed_model: Embedding):
        self.db = database
        self.embed = embed_model

    def query(self, query: str):
        conn = self.db.connect_langchain()
        results = conn.similarity_search(query=query,k=10)

        rag_query = ' '.join([doc.page_content for doc in results])

        return rag_query

    async def aquery(self, query: str):
        conn = self.db.connect_langchain()
        results = await conn.asimilarity_search(query=query,k=10)

        rag_query = ' '.join([doc.page_content for doc in results])

        return rag_query
