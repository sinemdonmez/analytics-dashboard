#!/bin/bash
set -e

echo "⏳ Waiting for DB to be ready..."

MAX_RETRIES=20
RETRY=0

until pg_isready -h db -p 5432 -U postgres; do
  RETRY=$((RETRY+1))
  echo "⏳ [$RETRY/$MAX_RETRIES] Waiting for Postgres to accept connections..."
  if [ "$RETRY" -ge "$MAX_RETRIES" ]; then
    echo "❌ Reached max retries. Exiting."
    exit 1
  fi
  sleep 2
done

echo "✅ Postgres is ready."

echo "📦 Seeding database..."
python3 src/app/data_gen.py

echo "🚀 Starting Flask server..."
exec python3 src/app/app.py
