#!/bin/bash
podman run --rm -it -p 8000:8000 ghcr.io/containers/ramalama run llama3.1:8b-instruct --api --port 8000
