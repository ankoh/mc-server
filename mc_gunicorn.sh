#!/usr/bin/env bash

# Export environment variables
export MENDELEY_CACHE_CONFIG=$(dirname "$0")/config.yml

# Run gunicorn
gunicorn -w 1 mendeleycache.app:app
