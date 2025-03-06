from langchain_community.document_loaders import PyPDFDirectoryLoader, WebBaseLoader
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)
from docling.document_converter import DocumentConverter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

import logging

logging.basicConfig(level=logging.INFO)


class RagRetriever:
    def __init__(self):
        self.PDFDOCSPATH = os.getenv("PDFDOCSPATH")
        self.COLLECTION_NAME = os.getenv("COLLECTION_NAME")
        self.DB_DIR = os.getenv("DB_DIR")
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.logger = logging.getLogger(__name__)

    def create_rag_from_docs_using_docling(self):
        # Get all PDF file paths in the directory
        pdf_files = [
            os.path.join(self.PDFDOCSPATH, f)
            for f in os.listdir(self.PDFDOCSPATH)
            if f.endswith(".pdf")
        ]

        self.logger.info("Starting document processing.")

        converter = DocumentConverter()
        markdown_documents = []

        for pdf in pdf_files:
            try:
                markdown = converter.convert(pdf).document.export_to_markdown()
                markdown_documents.append(markdown)
            except Exception as e:
                self.logger.error(f"Error processing {pdf}: {e}")

        # Join all Markdown content
        final_markdown = "\n\n".join(markdown_documents)

        headers_to_split_on = [("#", "Header 1"), ("##", "Header 2")]

        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
        splits = markdown_splitter.split_text(final_markdown)

        # === Vector Store ====
        Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=self.DB_DIR,
            collection_name=self.COLLECTION_NAME,
        )

    def create_rag_from_docs(self):

        # ==== Documents Loader ====
        loader = PyPDFDirectoryLoader(self.PDFDOCSPATH)
        docs = loader.load()

        # ==== Splitter ====
        text_spliter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=50, add_start_index=True
        )
        splits = text_spliter.split_documents(docs)

        # === Vector Store ====
        Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=self.DB_DIR,
            collection_name=self.COLLECTION_NAME,
        )

    def create_rag_from_urls(self, urls):
        # Load documents
        docs = [WebBaseLoader(url).load() for url in urls]
        docs_list = [item for sublist in docs for item in sublist]

        # Split documents into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=500, chunk_overlap=50, add_start_index=True
        )
        splits = text_splitter.split_documents(docs_list)

        # === Vector Store ====
        Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=self.DB_DIR,
            collection_name=self.COLLECTION_NAME,
        )

    def get_vector_store(self):
        vector_store = Chroma(
            embedding_function=self.embeddings,
            persist_directory=self.DB_DIR,
            collection_name=self.COLLECTION_NAME,
        )

        return vector_store

    def get_retriever(self):

        vector_store = self.get_vector_store()

        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5},
        )

        return retriever


rag_retriever = RagRetriever()
retriever = rag_retriever.get_retriever()

if __name__ == "__main__":
    rag = RagRetriever()
    print(rag.PDFDOCSPATH)
    # urls = [
    #     "https://www.cloudcustomsolutions.com/services/",
    #     "https://www.cloudcustomsolutions.com/products/",
    #     "https://www.cloudcustomsolutions.com/about-us/",
    #     "https://www.cloudcustomsolutions.com/business-matchmaking-software/",
    #     "https://www.cloudcustomsolutions.com/blog/",
    # ]
    # rag.create_rag_from_docs()
    # rag.create_rag_from_urls(urls)
    rag.create_rag_from_docs_using_docling()
