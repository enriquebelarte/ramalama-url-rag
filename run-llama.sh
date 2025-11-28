#!/bin/bash
MODEL=${1:-llama3.1:8b}
echo "Starting Ramalama with model: $MODEL"
podman run --rm -it -p 8000:8080 quay.io/ramalama/ramalama ramalama serve "$MODEL" --port 8080
