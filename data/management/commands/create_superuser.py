import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Automatically create a superuser using environment variables"

    def handle(self, *args, **options):
        # Get the environment variables
        su_email = os.getenv('DJANGO_SU_EMAIL')
        su_name = os.getenv('DJANGO_SU_NAME')
        su_password = os.getenv('DJANGO_SU_PASSWORD')

        # Check if all required environment variables are present
        if not su_email or not su_name or not su_password:
            self.stdout.write(self.style.ERROR('Environment variables DJANGO_SU_EMAIL, DJANGO_SU_NAME, and DJANGO_SU_PASSWORD are required to create a superuser.'))
            return

        # Get the User model
        User = get_user_model()

        # Check if a superuser with the given username or email already exists
        if User.objects.filter(username=su_name).exists() or User.objects.filter(email=su_email).exists():
            self.stdout.write(self.style.WARNING(f"A superuser with username '{su_name}' or email '{su_email}' already exists."))
        else:
            # Create the superuser
            User.objects.create_superuser(
                username=su_name,
                email=su_email,
                password=su_password
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser '{su_name}' created successfully."))