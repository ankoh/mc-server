__author__ = 'kohn'

import unittest
from unittest import TestLoader
from mendeleycache.utils.files import get_relative_path
import logging

# Disable logging for tests
logging.disable(logging.CRITICAL)

# Get project root path
project_root = get_relative_path(".")

# Prepare
loader = TestLoader()
runner = unittest.TextTestRunner(verbosity=2)

# Create suites
all = loader.discover(start_dir=project_root)

# Run suites
runner.run(all)
