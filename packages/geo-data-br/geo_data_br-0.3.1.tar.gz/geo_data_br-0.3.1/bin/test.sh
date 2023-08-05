#!/bin/bash
cd $(git rev-parse --show-toplevel)
set -o pipefail
set -e

if [[ $BUILD ]]; then docker-compose build; fi
docker-compose run --rm geo_data_br pytest -s "$@"
if [[ $CLEANUP ]]; then docker-compose stop; fi
