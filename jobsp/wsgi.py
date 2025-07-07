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
            # Create superuser with explicit staff and active flags
            admin_user = User.objects.create_superuser(
                username="admin", 
                email="admin@example.com", 
                password="admin123"
            )
            # Ensure the user is properly configured for admin access
            admin_user.is_staff = True
            admin_user.is_active = True
            admin_user.is_superuser = True
            admin_user.save()
            print("✅ Superuser created: admin@example.com / admin123")
        else:
            # Ensure existing admin user has proper permissions
            existing_admin = User.objects.get(username="admin")
            if not existing_admin.is_staff:
                existing_admin.is_staff = True
                existing_admin.is_active = True
                existing_admin.save()
                print("✅ Fixed existing admin user permissions")
            print("ℹ️ Superuser already exists.")

    except Exception as e:
        print("❌ Error running startup setup:", e)
