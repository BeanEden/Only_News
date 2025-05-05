#!/bin/sh

# Attente active de MySQL (si besoin)
echo "⏳ Attente de la base de données..."
until nc -z mysql 3306; do
  sleep 1
done
echo "✅ Base de données disponible"

# Migration Django
echo "🚀 Migration Django..."
python manage.py migrate

# Création du superuser si pas déjà présent
echo "👤 Création superuser admin..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "adminpass")
EOF

# Lancement du serveur
echo "🌍 Lancement du serveur Django..."
exec python manage.py runserver 0.0.0.0:8000
