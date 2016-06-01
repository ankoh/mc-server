#!/bin/bash

PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin
PYTHONPATH=/srv/mc/

# Trigger pipeline runner
python -m mendeleycache.runner pipeline
