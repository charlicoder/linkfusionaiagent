#!/bin/bash

# Exit on error
set -e

# Optional: Run migrations, wait for DB, etc.
# echo "Running pre-start tasks..."

# Start the FastAPI app using Uvicorn
exec uvicorn api:app --host 0.0.0.0 --port 8002