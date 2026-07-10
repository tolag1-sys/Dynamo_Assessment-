#!/bin/bash
# Plain pytest. pytest and pytest-json-ctrf are baked into the environment image,
# so there are no installs at verify time.
set -euo pipefail
cd "$(dirname "$0")"
pytest -q test_outputs.py
