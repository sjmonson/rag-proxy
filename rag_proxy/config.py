from pydantic import Field
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    upstream: str = Field(alias='PROXY_UPSTREAM')
    embed_upstream: str = Field(alias='EMBED_UPSTREAM')
    embed_model: str = Field(alias='EMBED_MODEL')
    database_name: str = Field(alias='DB_NAME')
    database_host: str = Field(default='localhost', alias='DB_HOST')
    database_port: int = Field(default=19530, alias='DB_PORT')
