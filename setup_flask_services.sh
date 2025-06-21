#!/usr/bin/env bash

# setup_flask_services.sh: Build and launch Flask-encapsulated services.

set -e

# Navigate to script directory (project root)
cd "$(dirname "$0")"

echo "Building and starting Flask-wrapped microservices..."
docker-compose up --build