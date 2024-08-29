from langchain_milvus import Milvus
from langchain_core.embeddings import Embeddings
from rag_proxy.caikit import CaiKitEmbeddings

def milvus_connect(
        host: str,
        port: str | int,
        embedding_model: Embeddings,
        name: str = 'default'
) -> Milvus:
    db = Milvus(
        embedding_model,
        collection_name=name,
        connection_args={"host": host, "port": port},
    )
    return db

def caikit_connect(endpoint: str, model_name: str) -> CaiKitEmbeddings:
    return CaiKitEmbeddings(endpoint, model_name)
