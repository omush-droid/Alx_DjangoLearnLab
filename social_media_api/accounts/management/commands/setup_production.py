from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.management import call_command
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Setup production environment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a superuser account',
        )
        parser.add_argument(
            '--collect-static',
            action='store_true',
            help='Collect static files',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Setting up production environment...'))

        # Run migrations
        self.stdout.write('📊 Running database migrations...')
        call_command('migrate', verbosity=0)
        self.stdout.write(self.style.SUCCESS('✅ Migrations completed'))

        # Collect static files
        if options['collect_static']:
            self.stdout.write('📦 Collecting static files...')
            call_command('collectstatic', '--noinput', verbosity=0)
            self.stdout.write(self.style.SUCCESS('✅ Static files collected'))

        # Create superuser
        if options['create_superuser']:
            self.stdout.write('👤 Creating superuser...')
            if not User.objects.filter(is_superuser=True).exists():
                username = input('Username: ')
                email = input('Email: ')
                password = input('Password: ')
                User.objects.create_superuser(username=username, email=email, password=password)
                self.stdout.write(self.style.SUCCESS('✅ Superuser created'))
            else:
                self.stdout.write(self.style.WARNING('⚠️ Superuser already exists'))

        # Check environment variables
        self.stdout.write('🔧 Checking environment variables...')
        required_vars = ['SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS']
        missing_vars = []
        
        for var in required_vars:
            if not os.environ.get(var):
                missing_vars.append(var)
        
        if missing_vars:
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️ Missing environment variables: {", ".join(missing_vars)}'
                )
            )
        else:
            self.stdout.write(self.style.SUCCESS('✅ All required environment variables set'))

        # Production checklist
        self.stdout.write('\n📋 Production Deployment Checklist:')
        checklist = [
            'Set DEBUG=False in production',
            'Configure ALLOWED_HOSTS with your domain',
            'Set up HTTPS/SSL certificate',
            'Configure database backups',
            'Set up monitoring and logging',
            'Test all API endpoints',
            'Configure media file storage',
            'Set up error tracking (e.g., Sentry)',
        ]
        
        for item in checklist:
            self.stdout.write(f'  • {item}')

        self.stdout.write(self.style.SUCCESS('\n🎉 Production setup completed!'))