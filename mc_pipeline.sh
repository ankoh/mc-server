#!/bin/bash

# Export environment variables
export MENDELEY_CACHE_CONFIG=$(dirname "$0")/sample_config.yml

# Trigger pipeline runner
python -m mendeleycache.runner pipeline