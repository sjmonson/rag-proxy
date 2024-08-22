import os
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_milvus import Milvus
from pymilvus import MilvusClient
from pymilvus import connections, utility

class VectorDB:
    def __init__(self, host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), collection_name="default", embedding_model=os.getenv("EMBED_MODEL")):
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
        db = Milvus(
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
            db = Milvus.from_documents(
                documents,
                self.embedding_model,
                collection_name=self.collection_name,
                connection_args={"host": self.host, "port": self.port},
            )
            print("DB populated")
        else:
            print("DB already populated")
            db = Milvus(
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
