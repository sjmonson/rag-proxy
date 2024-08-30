import time
from pydantic import BaseModel
from langchain_core.vectorstores import VectorStore
from langchain_core.embeddings import Embeddings

class RetrievalUsage(BaseModel):
    """ Timing model for VectorDB Retrieval """
    embedding: float
    database: float

class RetrievalResponse(BaseModel):
    """ Response model for VectorDB Retrieval """
    response: str
    embedding: list[float]
    usage: RetrievalUsage

class RetrievalAugmentation(object):
    """ A VectorDB Retrieval factory """
    def __init__(
            self,
            database: VectorStore,
            embedding: Embeddings,
            prompt: str,
            top_k: int = 10
    ):
        self.db = database
        self.embed = embedding
        self.prompt = prompt
        self.k = top_k

    def query(self, query: str):
        # TODO: Figure out if we can do this with a langchain
        time_start = time.time()
        vec = self.embed.embed_query(query)
        time_embed = time.time()
        results = self.db.similarity_search_by_vector(vec, self.k)
        time_db = time.time()

        retrieved = ' '.join([doc.page_content for doc in results])
        final = self.prompt.format(context=retrieved, question=query)
        timing = RetrievalUsage(
            embedding=time_embed-time_start,
            database=time_db-time_embed
        )

        return RetrievalResponse(response=final, embedding=vec, usage=timing)
