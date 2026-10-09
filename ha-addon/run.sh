#!/bin/sh
# Entry point for the Home Assistant add-on: map add-on options to env vars.
set -e

OPTIONS=/data/options.json
if [ -f "$OPTIONS" ]; then
    QOBUZPROXY_LOG_LEVEL=$(python -c \
        'import json, sys; print(json.load(open(sys.argv[1])).get("log_level", "info"))' \
        "$OPTIONS")
    export QOBUZPROXY_LOG_LEVEL
fi

exec qobuz-proxy
