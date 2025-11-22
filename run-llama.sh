#!/bin/bash
podman run --rm -it -p 8000:8080   quay.io/ramalama/ramalama ramalama serve llama3.1:8b --port 8080
