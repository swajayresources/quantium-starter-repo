#!/bin/bash
set -e

# Activate the virtual environment
source ../venv/Scripts/activate

# Execute the test suite
pytest test_app.py -v --headless

# pytest exits with 0 on success, non-zero on failure.
# set -e ensures any non-zero exit code propagates immediately.
# Explicitly return 0 on success.
exit 0
