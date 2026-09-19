#!/bin/bash

set -e

echo "Esperando PostgreSQL..."

until docker exec postgres_db pg_isready -U root -d postgres > /dev/null 2>&1; do
    sleep 2
done

echo "PostgreSQL está listo."

echo "Restaurando backup..."

cat backup_postgres_full.dump | docker exec -i postgres_db pg_restore \
    -U root \
    -d postgres \
    --clean \
    --if-exists \
    --no-owner

echo "Backup restaurado correctamente."