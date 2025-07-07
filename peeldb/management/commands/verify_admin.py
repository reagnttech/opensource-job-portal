"""
Django management command to verify and fix admin user setup.
Usage: python manage.py verify_admin
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction


class Command(BaseCommand):
    help = 'Verify and fix admin user setup for proper admin login'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Fix any issues found with the admin user',
        )
        parser.add_argument(
            '--create',
            action='store_true',
            help='Create admin user if it does not exist',
        )

    def handle(self, *args, **options):
        User = get_user_model()
        
        self.stdout.write(self.style.SUCCESS('🔍 Verifying admin user setup...'))
        
        # Check if admin user exists
        try:
            admin_user = User.objects.get(username="admin")
            self.stdout.write(f"✅ Admin user found: {admin_user.email}")
            
            # Check admin user properties
            issues = []
            if not admin_user.is_staff:
                issues.append("is_staff=False")
            if not admin_user.is_superuser:
                issues.append("is_superuser=False")
            if not admin_user.is_active:
                issues.append("is_active=False")
            
            if issues:
                self.stdout.write(
                    self.style.WARNING(f"❌ Issues found: {', '.join(issues)}")
                )
                
                if options['fix']:
                    with transaction.atomic():
                        admin_user.is_staff = True
                        admin_user.is_superuser = True
                        admin_user.is_active = True
                        admin_user.save()
                    self.stdout.write(
                        self.style.SUCCESS("✅ Fixed admin user permissions!")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING("Use --fix flag to resolve these issues")
                    )
            else:
                self.stdout.write(
                    self.style.SUCCESS("✅ Admin user has correct permissions")
                )
                
            # Check if password is set
            if admin_user.password:
                self.stdout.write("✅ Admin user has password set")
            else:
                self.stdout.write(
                    self.style.ERROR("❌ Admin user has no password!")
                )
                
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR("❌ Admin user does not exist!")
            )
            
            if options['create']:
                self.stdout.write("Creating admin user...")
                try:
                    with transaction.atomic():
                        admin_user = User.objects.create_superuser(
                            username="admin",
                            email="admin@example.com", 
                            password="admin123"
                        )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✅ Created admin user: {admin_user.email} / admin123"
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Error creating admin user: {e}")
                    )
            else:
                self.stdout.write(
                    self.style.WARNING("Use --create flag to create admin user")
                )
        
        # Test authentication backend
        self.stdout.write(self.style.SUCCESS('\n🔍 Testing authentication...'))
        
        from django.contrib.auth import authenticate
        try:
            user = authenticate(username="admin@example.com", password="admin123")
            if user:
                if user.is_staff:
                    self.stdout.write(
                        self.style.SUCCESS("✅ Admin authentication successful!")
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR("❌ User authenticated but not staff!")
                    )
            else:
                self.stdout.write(
                    self.style.ERROR("❌ Authentication failed!")
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Authentication error: {e}")
            )
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n📋 Summary:'))
        self.stdout.write("Admin login URL: /admin/")
        self.stdout.write("Admin credentials: admin@example.com / admin123")
        self.stdout.write("Use --fix to resolve permission issues")
        self.stdout.write("Use --create to create missing admin user") 