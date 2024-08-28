from caikit_nlp_client import HttpClient

from rag_proxy.embedding import *

class CaiKitEmbedding(Embedding):
    def __init__(self, host: str, model_name: str):
        self.host = host
        self.model = model_name

    async def aembedding(self, text: str) -> EmbeddingResult:
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

        vec: Vector = response['result']['data']['values']
        input_tokens: int = response['input_token_count']

        return EmbeddingResult(embedding=vec, input_tokens=input_tokens)
