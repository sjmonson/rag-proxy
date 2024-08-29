from caikit_nlp_client import HttpClient
from langchain_core.embeddings import Embeddings

class CaiKitEmbeddings(Embeddings):
    def __init__(self, host: str, model_name: str):
        self.host = host
        self.model = model_name

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        client = HttpClient(self.host)

        response = client.embedding_tasks(
            model_id=self.model,
            texts=texts,
            # TODO: Do we want more tunables?
            # parameters={
            #     "truncate_input_tokens": self.model_max_input_tokens
            # },
            timeout = 60
        )

        return response['result']['data']['values']

    def embed_query(self, text: str) -> list[float]:
        client = HttpClient(self.host)

        response = client.embedding(
            model_id=self.model,
            text=text,
            # TODO: Do we want more tunables?
            # parameters={
            #     "truncate_input_tokens": self.model_max_input_tokens
            # },
            timeout = 60
        )

        vectors = [ res['data']['values'] for res in response['results']['vectors'] ]

        return vectors
