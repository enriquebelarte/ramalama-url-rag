#!/usr/bin/env python3

import subprocess
import sys
import argparse

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
def load_urls_from_file(file_path="urls.txt"):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Please create it with one URL per line.")
        sys.exit(1)

parser = argparse.ArgumentParser(description="RAG with Ramalama")
parser.add_argument("file_path", nargs="?", default="urls.txt", help="Path to the file containing URLs")
parser.add_argument("--model", default="llama3.1:8b-instruct", help="Model name to use")
args = parser.parse_args()

urls = load_urls_from_file(args.file_path)
print(f"Loaded {len(urls)} URLs from {args.file_path}.")
print("Downloading and parsing URLs...")
documents = SimpleWebPageReader().load_data(urls)

# 2. Build a vector index
print("Building vector index...")
index = VectorStoreIndex.from_documents(documents)

# 3. Connect to local Ramalama LLM via OpenAI API protocol
llm = OpenAI(
    api_key="dummy",  # required but unused
    api_base="http://localhost:8000/v1",
    model=args.model,
)

query_engine = index.as_query_engine(llm=llm)

# 4. Ask your question
question = "Explain containerization in simple terms based on the pages you loaded."
print(f"Query: {question}\n")

response = query_engine.query(question)

print("\n=== RAG Answer ===\n")
print(response)
