#!/usr/bin/env bash

# First check the environment variables
if [ -z "$MC_DATABASE_PATH" ]; then
    echo "You need to provide MC_DATABASE_PATH as environment variable"
    exit 1
fi

# Prepare application
python -m mendeleycache.runner prepare

# Then fire the rest of the commands
exec "$@"
