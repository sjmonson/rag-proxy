import httpx
import asyncio
from fastapi import FastAPI
from pydantic import config
from starlette.requests import Request
from starlette.responses import StreamingResponse
from starlette.background import BackgroundTask
import logging

from vllm.entrypoints.openai.protocol import (ChatCompletionRequest,
                                              ChatCompletionResponse,
                                              CompletionRequest)
from rag_proxy.config import Config
from rag_proxy.ra import RetrievalAugmentation
# TODO: Make DB and Embedding selectors
from rag_proxy.utility import caikit_connect, milvus_connect

# TODO: Put prompt in config
template = """<s>[INST]
You are a friendly documentation search bot.
Use following piece of context to answer the question.
If the context is empty, try your best to answer without it.
Never mention the context.
Try to keep your answers concise unless asked to provide details.

Context: {context}
Question: {question}
[/INST]</s>
Answer:
"""

config = Config()

logger = logging.getLogger(__name__)

# Our upstream client
client = httpx.AsyncClient(base_url=config.upstream, timeout=None)

app = FastAPI()

async def ask(prompt: str) -> str:
    embedding = caikit_connect(config.embed_upstream, config.embed_model)
    database = milvus_connect(config.database_host, config.database_port, embedding, config.database_name)
    ra = RetrievalAugmentation(database, embedding, template, 10)

    result = ra.query(prompt)
    # TODO: Log timings
    return result.response

@app.post("/v1/completions")
async def create_completion(request: CompletionRequest, raw_request: Request):
    if isinstance(request.prompt, str):
        prompts = [request.prompt]
    else:
        prompts = request.prompt

    # Perform Embedding and Retrieval on prompt
    request.prompt = await asyncio.gather(*[ask(prompt) for prompt in prompts])
    #logger.info(repr(request.prompt))
    #print(repr(request.prompt))

    # Re-encode updated message body
    body = request.model_dump_json(exclude_defaults=True).encode("utf-8")

    # Update headers to match new body
    headers = raw_request.headers.mutablecopy()
    headers["content-length"] = str(len(body))

    # Craft upstream request
    url = httpx.URL(path=raw_request.url.path,
                    query=raw_request.url.query.encode("utf-8"))
    rp_req = client.build_request(raw_request.method, url,
                                  headers=headers.raw,
                                  content=body)

    # Send request upstream
    rp_resp = await client.send(rp_req, stream=True)

    # Stream back the upstream response
    return StreamingResponse(
        rp_resp.aiter_raw(),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        background=BackgroundTask(rp_resp.aclose),
    )

# TODO: /v1/chat/completions

# TODO: Generic route that passes to upstream
# async def _reverse_proxy(request: Request):
#     url = httpx.URL(path=request.url.path,
#                     query=request.url.query.encode("utf-8"))
#     rp_req = client.build_request(request.method, url,
#                                   headers=request.headers.raw,
#                                   content=await request.body())
#     rp_resp = await client.send(rp_req, stream=True)
#     return StreamingResponse(
#         rp_resp.aiter_raw(),
#         status_code=rp_resp.status_code,
#         headers=rp_resp.headers,
#         background=BackgroundTask(rp_resp.aclose),
#     )
#
# app.add_route("/{path:path}", _reverse_proxy, ["GET", "POST"])
