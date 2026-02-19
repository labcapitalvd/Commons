#!/usr/bin/env bash
if [[ "$1" == "fetcher" ]]; then
  FETCHER=$(date +%s)
  shift
else
  FETCHER=1
fi

if [[ "$1" == "packages" ]]; then
  PACKAGES=$(date +%s)
  shift
else
  PACKAGES=1
fi

(
  cd Auth && docker compose build \
    --build-arg FETCHER="$FETCHER" "$@" \
    --build-arg PACKAGES="$PACKAGES" "$@" &&
    docker push labcapital/apps:Auth
)
