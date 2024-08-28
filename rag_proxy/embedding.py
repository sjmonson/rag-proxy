from pydantic import BaseModel

type Scalar = int | float
type Vector = list[Scalar]

class EmbeddingResult(BaseModel):
    # TODO: What other information do we want
    embedding: Vector
    input_tokens: int

class Embedding(object):
    # TODO: Define a standard interface for all embeddings
    pass
