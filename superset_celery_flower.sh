#!/bin/bash

# Special Consideration for macOS
# On macOS (evident from the file paths in your errors), remember 
# to address the fork safety issue when restarting

# Load environment variables from .env file
# export "$(grep -v '^#' .env | xargs)"
set -o allexport
source .env
set +o allexport

export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

export SUPERSET_CONFIG_PATH=./superset_config.py

celery -A superset.tasks.celery_app:app flower --port=5555