# Ramalama Local RAG with URL Indexing

This project allows you to perform Retrieval-Augmented Generation (RAG) using a local LLM served by **Ramalama**. You can provide a list of URLs, index their content, and ask questions based on that content without sending data to external AI providers.

## Prerequisites

-   **Python 3.x**
-   **Podman** (for running the Ramalama container)
-   **Ramalama** installed or configured to run via container.

## Project Structure

-   `rag_url_query.py`: Python script that downloads content from URLs, creates a vector index, and queries the local LLM.
-   `run-llama.sh`: Helper script to start the Ramalama server using Podman.
-   `urls.txt`: A text file containing the list of URLs to index (one per line).

## Setup & Usage

### 1. Start the Ramalama Server

First, you need to have the local LLM running and listening for API requests. The included script starts a container serving the `llama3.1:8b` model on port 8080 (mapped to 8000 inside the container protocol).

```bash
./run-llama.sh
```

*Note: Keep this terminal open or run it in the background.*

### 2. Configure Sources

Edit the `urls.txt` file to include the web pages you want the LLM to read.

```text
https://en.wikipedia.org/wiki/Containerization
https://opensource.com/article/18/10/introduction-containers
```

### 3. Run the Query Script

In a new terminal window, run the Python script. It will automatically install necessary Python dependencies (`llama-index`, etc.) on the first run.

```bash
python3 rag_url_query.py
```

By default, it reads from `urls.txt`. You can also specify a different file:

```bash
python3 rag_url_query.py my_custom_urls.txt
```

## How It Works

1.  **Ingest**: The script reads URLs from the text file and fetches their content.
2.  **Index**: It creates a local vector store index from the text content.
3.  **Query**: It sends your question (hardcoded in the script currently) + relevant context to the local Ramalama API (`http://localhost:8000/v1`).
4.  **Answer**: The LLM generates an answer based strictly on the provided context.

## Troubleshooting

-   **Connection Refused**: Ensure `./run-llama.sh` is running and accessible at `http://localhost:8000`.
-   **Missing Packages**: The script tries to auto-install packages. If this fails, manually install:
    ```bash
    pip install llama-index llama-index-llms-openai llama-index-readers-web
    ```
