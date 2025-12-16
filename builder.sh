#!/usr/bin/env bash
if [[ "$1" == "cachebuster" ]]; then
    CACHEBUST=$(date +%s)
    shift
else
    CACHEBUST=1
fi

cd Auth && docker compose build --build-arg CACHEBUST=$CACHEBUST "$@" && docker push labcapital/apps:Auth