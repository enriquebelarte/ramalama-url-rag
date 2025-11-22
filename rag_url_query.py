#!/usr/bin/env python3

import subprocess
import sys

REQUIRED_PACKAGES = [
    "llama-index",
    "llama-index-llms-openai",
    "llama-index-readers-web",
]

# --- Auto-install missing packages ---
def install(package):
    print(f"Installing missing package: {package}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for pkg in REQUIRED_PACKAGES:
    try:
        __import__(pkg.replace("-", "_"))
    except ImportError:
        install(pkg)

# --- Actual RAG code begins here ---
from llama_index.core import VectorStoreIndex
from llama_index.readers.web import SimpleWebPageReader
from llama_index.llms.openai import OpenAI

# 1. Load documents from URLs
urls = [
    "https://en.wikipedia.org/wiki/Containerization",
    "https://opensource.com/article/18/10/introduction-containers"
]
print("Downloading and parsing URLs...")
documents = SimpleWebPageReader().load_data(urls)

# 2. Build a vector index
print("Building vector index...")
index = VectorStoreIndex.from_documents(documents)

# 3. Connect to local Ramalama LLM via OpenAI API protocol
llm = OpenAI(
    api_key="dummy",  # required but unused
    api_base="http://localhost:8000/v1",
    model="llama3.1:8b-instruct",
)

query_engine = index.as_query_engine(llm=llm)

# 4. Ask your question
question = "Explain containerization in simple terms based on the pages you loaded."
print(f"Query: {question}\n")

response = query_engine.query(question)

print("\n=== RAG Answer ===\n")
print(response)
