#!/usr/bin/env bash

# Exit on error and print commands
set -e
set -x

# Get the absolute path to the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Add the project root to PYTHONPATH
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH:-}"

# Let the DB start
python "${PROJECT_ROOT}/app/backend_pre_start.py"

# Run migrations (uncomment if needed)
# alembic upgrade head

# Create initial data in DB
python "${PROJECT_ROOT}/app/initial_data.py"

# Print success message
echo "Prestart script completed successfully!"