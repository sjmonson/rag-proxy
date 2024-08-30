# rag-proxy

A middle-layer designed to insert Retrieval Augmented Generation (RAG) into an existing inference endpoint.

## Requirements

### Install

- Python 3.12 or newer

### Run

- An OpenAI API-compatible inference server; like [vLLM](https://github.com/vllm-project/vllm)
- A [Caikit](https://github.com/caikit/caikit) embeddings server
- A Milvus database

### Develop

- [poetry](https://python-poetry.org/docs/#installation)

## Getting Started

``` sh
# Checkout Repo
git clone https://github.com/sjmonson/rag-proxy.git
cd rag-proxy

# Create a Virtual Environment
python -m venv venv
source venv/bin/activate

# Install rag-proxy
pip install .
```

## Usage

```
usage: rag-proxy [-h] [-H HOST] [-p PORT]

RAG Proxy

options:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  Hostname to bind to, defaults to localhost
  -p PORT, --port PORT  Port to bind to, defaults to 8000
```

### TODO Loading the Database

### Configuration

Copy the example `.env` and edit to match your configuration.

``` sh
cp .env-example .env
```

### Running

To run a proxy server on `127.0.0.1:8002`:

``` sh
rag-proxy -H 127.0.0.1 -p 8002
```

Assuming all your various endpoints are set up correctly, you can now run inference requests against the proxy:

``` sh
$ curl http://127.0.0.1:8002/v1/completions -H "Content-Type: application/json" \
    -d '{"model": "ibm-granite/granite-8b-code-instruct-128k", "prompt": "What is the meaning of life" }' | jq .choices[0].text
"Hello! I'm glad to help you out.\n\nThe meaning of life is"
```
