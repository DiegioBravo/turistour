#!/bin/bash

echo "=========================================="
echo "  INICIANDO DEPLOY AUTOMÁTICO EN RENDER"
echo "=========================================="

# ------------------------------
# 1. Aplicar makemigrations
# ------------------------------
echo "➡ Ejecutando makemigrations..."
python manage.py makemigrations --noinput

# ------------------------------
# 2. Aplicar migrate
# ------------------------------
echo "➡ Ejecutando migrate..."
python manage.py migrate --noinput

# ------------------------------
# 3. Crear superusuario automáticamente (si no existe)
# ------------------------------
echo "➡ Verificando superusuario 'admin'..."

python manage.py shell << 'EOF'
from django.contrib.auth.models import User

username = "admin"
password = "123456"
email = "admin@example.com"

if not User.objects.filter(username=username).exists():
    print("➡ Creando superusuario...")
    User.objects.create_superuser(username=username, email=email, password=password)
else:
    print("✔ Superusuario ya existe, no se crea.")
EOF

# ------------------------------
# 4. Arrancar servidor Gunicorn
# ------------------------------
echo "=========================================="
echo "  INICIANDO GUNICORN..."
echo "=========================================="

gunicorn webturismo.wsgi:application --bind 0.0.0.0:$PORT
