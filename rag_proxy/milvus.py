import os
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_milvus import Milvus as LangMilvus
from pymilvus import MilvusClient
from pymilvus import connections, utility

from rag_proxy.vectordb import VectorDB

from .config import Config

config = Config()

class Milvus(VectorDB):
    def __init__(self, host=config.database_host, port=config.database_port, collection_name=config.database_name, embedding_model=config.embed_model):
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.embedding_model = SentenceTransformerEmbeddings(model_name=embedding_model)

    def connect(self):
        # Connection logic
        print(f"Connecting to {self.host}:{self.port}...")
        self.client = MilvusClient(uri=f"http://{self.host}:{self.port}")
        return self.client

    def connect_langchain(self):
        db = LangMilvus(
            self.embedding_model,
            collection_name=self.collection_name,
            connection_args={"host": self.host, "port": self.port},
        )
        return db

    def populate_db(self, documents):
        # Logic to populate the VectorDB with vectors
        print(f"Populating VectorDB with vectors...")
        connections.connect(host=self.host, port=self.port)
        if not utility.has_collection(self.collection_name):
            print("Populating VectorDB with vectors...")
            db = LangMilvus.from_documents(
                documents,
                self.embedding_model,
                collection_name=self.collection_name,
                connection_args={"host": self.host, "port": self.port},
            )
            print("DB populated")
        else:
            print("DB already populated")
            db = LangMilvus(
                self.embedding_model,
                collection_name=self.collection_name,
                connection_args={"host": self.host, "port": self.port},
            )
        return db

    def clear_db(self):
        print(f"Clearing VectorDB...")
        try:
            self.client.drop_collection(self.collection_name)
            print("Cleared DB")
        except:
            print("Couldn't clear the collection possibly because it doesn't exist")
