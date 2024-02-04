#!/bin/bash

while true; do
  if grep -rq "pytest\.mark"; then
    entrypoint="poetry run poe test_marked -m 'dev'"
  else
    entrypoint="poetry run poe test"
  fi
  docker compose -f tests/docker/docker-compose.yml run --rm --service-ports --entrypoint "$entrypoint" package-$1
  inotifywait -qq -r -e moved_to -e create -e modify -e delete -e close_write .
done
