#/bin/bash

set -e

# Error if DATABASE_URL isn't set
if [ -z "$DATABASE_URL" ]; then
    echo "Error: DATABASE_URL is not set"
    exit 1
fi

query="SELECT EXISTS(SELECT 1 FROM pg_available_extensions WHERE name = 'vector')::int;"
is_installed=$(psql $DATABASE_URL -t -c "$query")
is_installed=$(echo $is_installed | xargs) # Trim whitespace
if [ "$is_installed" -ne "1" ]; then
    echo "The pg_vector extension isn't installed. Install it."
    exit 1
fi
psql $DATABASE_URL -c "CREATE EXTENSION vector;"