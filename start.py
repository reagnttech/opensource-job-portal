# start.py

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobsp.settings_server")
django.setup()

from django.contrib.auth import get_user_model
from django.core.management import call_command

print("👉 Running database migrations...")
call_command("migrate")

print("👉 Loading initial data fixtures...")
fixtures = ["industries", "qualification", "skills", "countries", "states", "cities"]
for fixture in fixtures:
    try:
        call_command("loaddata", fixture)
    except Exception as e:
        print(f"⚠️ Could not load fixture {fixture}: {e}")

print("👉 Creating default superuser...")
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="admin123"
    )
    print("✅ Superuser created.")
else:
    print("ℹ️ Superuser already exists.")

print("🚀 Starting Gunicorn server...")
os.system("gunicorn jobsp.wsgi:application --bind 0.0.0.0:8000")
