#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

function clean {
  rm -rf dist build .eggs .pytest_cache
  rm -rf episodekit.egg-info episodekit/__pycache__ tests/__pycache__
}

clean
uv build
uv run --isolated --no-project --with dist/*.whl --with pytest pytest -p no:cacheprovider tests
uv publish
# set UV_PUBLISH_TOKEN to the token (in the notes of pypi in vault) or use the username __token__ and the token as password
