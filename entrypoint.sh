#!/bin/sh

# Esperar a que la base de datos esté lista (opcional, pero recomendado en prod)
# o simplemente ejecutar migraciones.

echo "Applying database migrations..."
python manage.py migrate

echo "Starting server..."
exec "$@"
