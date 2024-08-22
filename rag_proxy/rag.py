from .db import VectorDB

def rag_query(query, db=None):
    if not db:
        db = VectorDB()
    conn = db.connect_langchain()
    results = conn.similarity_search(query=query,k=1)

    rag_query = ' '.join([doc.page_content for doc in results])

    return rag_query

async def arag_query(query, db=None):
    if not db:
        db = VectorDB()
    conn = db.connect_langchain()
    results = await conn.asimilarity_search(query=query,k=1)

    rag_query = ' '.join([doc.page_content for doc in results])

    return rag_query
