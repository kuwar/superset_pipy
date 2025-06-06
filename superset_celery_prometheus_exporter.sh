#!/bin/bash

# Special Consideration for macOS
# On macOS (evident from the file paths in your errors), remember 
# to address the fork safety issue when restarting

# Load environment variables from .env file
set -o allexport
source .env
set +o allexport

export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

export SUPERSET_CONFIG_PATH=./superset_config.py

celery-prometheus-exporter --broker=redis://localhost:6379/0