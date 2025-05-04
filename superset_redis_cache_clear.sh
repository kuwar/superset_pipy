#!/bin/bash

# Script to clear Redis caches for Superset

# Make sure Redis CLI is installed
# For Ubuntu/Debian: sudo apt-get install redis-tools
# For MacOS: brew install redis

echo "Clearing Redis caches for Superset..."

# Clear Redis DB 0 (Celery broker)
echo "Clearing Celery broker (Redis DB 0)..."
redis-cli -n 0 FLUSHDB

# Clear Redis DB 1 (Celery results backend)
echo "Clearing Celery results (Redis DB 1)..."
redis-cli -n 1 FLUSHDB

# Clear Redis DB 2 (Superset cache)
echo "Clearing Superset cache (Redis DB 2)..."
redis-cli -n 2 FLUSHDB

echo "All Redis caches have been cleared successfully."