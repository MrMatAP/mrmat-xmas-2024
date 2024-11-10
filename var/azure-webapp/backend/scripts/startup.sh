#!/bin/bash

echo "Starting on port $SERVER_PORT"
python -m uvicorn mrmat_xmas_2024.app:app --host 0.0.0.0 --port 8000
