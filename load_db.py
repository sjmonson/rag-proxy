#!/usr/bin/env python3

"""
Script to load PDFs into vector database.

Adapted from:
https://github.com/DS4SD/docling/blob/cde671cf34af6c1fd0da6a5bab20afbe6d57c5b1/examples/rag_langchain.ipynb
"""

import argparse
from enum import Enum
from typing import Iterator
from dotenv import load_dotenv
from rag_proxy.config import Config
from rag_proxy.utility import caikit_connect, milvus_connect
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document as LCDocument
from docling.document_converter import DocumentConverter
from pydantic import BaseModel

# TODO: Write your own chunker
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()
config = Config()


# TODO: Add more metadata
class DocumentMetadata(BaseModel):
    dl_doc_hash: str
    # source: str


class DoclingPDFLoader(BaseLoader):
    class ParseType(str, Enum):
        MARKDOWN = "markdown"
        # JSON = "json"

    def __init__(self, file_path: str | list[str], parse_type: ParseType) -> None:
        self._file_paths = file_path if isinstance(file_path, list) else [file_path]
        self._parse_type = parse_type
        self._converter = DocumentConverter()

    def lazy_load(self) -> Iterator[LCDocument]:
        for source in self._file_paths:
            dl_doc = self._converter.convert_single(source).output
            match self._parse_type:
                case self.ParseType.MARKDOWN:
                    text = dl_doc.export_to_markdown()
                # case self.ParseType.JSON:
                #     text = dl_doc.model_dump_json()
            lc_doc = LCDocument(
                page_content=text,
                metadata=DocumentMetadata(
                    dl_doc_hash=dl_doc.file_info.document_hash,
                ).model_dump(),
            )
            yield lc_doc


def parse_documents(paths: list[str]) -> list[LCDocument]:
    loader = DoclingPDFLoader(
        file_path=paths,
        parse_type=DoclingPDFLoader.ParseType.MARKDOWN,
    )

    return loader.load()

def split_documents(docs: list[LCDocument]) -> list[LCDocument]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=128
    )

    return text_splitter.split_documents(docs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Milvus Document Loader")

    parser.add_argument('--append', '-a', action='store_true',
                        help="Append documents without wiping database.")
    parser.add_argument('pdf', type=argparse.FileType('r'), nargs='+')

    args = parser.parse_args()

    print("Parsing documents to markdown...")
    markdown = parse_documents([path.name for path in args.pdf])

    print("Chunking documents")
    chunks = split_documents(markdown)

    print("Connecting to database and embeddings")
    embedding = caikit_connect(config.embed_upstream, config.embed_model)
    database = milvus_connect(config.database_host, config.database_port,
                              embedding, config.database_name, drop_old=args.append)

    print("Adding documents...")
    ids = database.add_documents(chunks)

    print("Added documents:", ids)
