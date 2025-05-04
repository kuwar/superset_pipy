#!/bin/bash

# Special Consideration for macOS
# On macOS (evident from the file paths in your errors), remember 
# to address the fork safety issue when restarting

# Load environment variables from .env file
export "$(grep -v '^#' .env | xargs)"

export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

export SUPERSET_CONFIG_PATH=./superset_config.py

gunicorn \
    -w 10 \
    -k gevent \
    --worker-connections 1000 \
    --timeout 120 \
    -b 0.0.0.0:8088 \
    --limit-request-line 0 \
    --limit-request-field_size 0 \
    "superset.app:create_app()"