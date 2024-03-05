#!/bin/bash
set -e

container_name="notes-rag-postgres"
container_image="pgvector/pgvector:pg16"

# Find the directory where this script lives.
here=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

# Check if the container is already running
matching_containers=$(docker ps -f "name=${container_name}" --quiet | wc -l)
if [ "$matching_containers" -eq "1" ]; then
  echo "Error: container with name $container_name is already running"
  printf "Shut down container? [y/N] "
  read response
  case "$response" in
    y* | Y* )
        docker stop "$container_name" > /dev/null
        ;;
    * )
        echo "Exiting"
        exit 1
        ;;
  esac
fi

# Start fresh container.
echo
echo "start-local-db: Starting postgres container"
echo "-------------------------------------------"

container_id=$(
    docker run \
    --name ${container_name} \
    -e POSTGRES_USER=notes-rag \
    -e POSTGRES_PASSWORD=notes-rag \
    -e POSTGRES_DB=documents \
    -d --rm \
    -p 6543:5432 \
    ${container_image}
)
sleep 1
echo "Container ID: $container_id"

# Run migrations.
echo
echo "start-local-db: Running setup"
echo "----------------------------------"
DATABASE_URL=postgresql://notes-rag:notes-rag@localhost:6543/documents $here/run-setup.sh