#!/usr/bin/env bash
# Wait for a service to be ready

TIMEOUT=60
STRICT=0
HOST=""
PORT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --timeout=*) TIMEOUT="${1#*=}"; shift ;;
    --strict) STRICT=1; shift ;;
    --) shift; break ;;
    *) HOST="$1"; PORT="${2:-}"; shift 2 ;;
  esac
done

echo "⌛ Waiting for $HOST:$PORT (timeout: $TIMEOUT seconds)"

start_ts=$(date +%s)
while :
do
  nc -z "$HOST" "$PORT" && break
  sleep 1
  current_ts=$(date +%s)
  elapsed_time=$((current_ts - start_ts))
  if [[ $elapsed_time -ge $TIMEOUT ]]; then
    echo "❌ Timeout! Service did not start in time."
    exit 1
  fi
done

echo "✅ Service $HOST:$PORT is up"
exec "$@"
