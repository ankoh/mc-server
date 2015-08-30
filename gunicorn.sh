#!/usr/bin/env bash

# Run gunicorn
gunicorn -w 1 mendeleycache.app:app
