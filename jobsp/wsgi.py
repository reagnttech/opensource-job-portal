import os
import sys
from django.core.wsgi import get_wsgi_application

# Set the settings module first
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobsp.settings_server")

# Get the WSGI application 
application = get_wsgi_application()

# Only run initialization in development or when explicitly requested
# In production, migrations should be run separately via build commands
if os.getenv("RUN_SETUP_ON_START") == "true":
    import django
    from django.core.management import call_command
    from django.contrib.auth import get_user_model

    try:
        print("🔧 Running initial setup...")

        # Run migrations
        call_command("migrate", interactive=False)

        # Load initial data
        call_command("loaddata", "industries", "qualification", "skills", "countries", "states", "cities")

        # Create superuser if not already created
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin123")
            print("✅ Superuser created: admin / admin123")
        else:
            print("ℹ️ Superuser already exists.")

    except Exception as e:
        print("❌ Error running startup setup:", e)
