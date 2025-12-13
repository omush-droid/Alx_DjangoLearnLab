from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Check production configuration'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Production Configuration Check')
        self.stdout.write('=' * 40)
        
        # Check DEBUG setting
        if settings.DEBUG == False:
            self.stdout.write(self.style.SUCCESS('✅ DEBUG = False'))
        else:
            self.stdout.write(self.style.ERROR('❌ DEBUG should be False in production'))
        
        # Check ALLOWED_HOSTS
        if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS != ['localhost', '127.0.0.1']:
            self.stdout.write(self.style.SUCCESS(f'✅ ALLOWED_HOSTS configured: {settings.ALLOWED_HOSTS}'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ ALLOWED_HOSTS should be configured for production'))
        
        # Check security settings
        security_checks = [
            ('SECURE_BROWSER_XSS_FILTER', True),
            ('X_FRAME_OPTIONS', 'DENY'),
            ('SECURE_CONTENT_TYPE_NOSNIFF', True),
        ]
        
        for setting_name, expected_value in security_checks:
            actual_value = getattr(settings, setting_name, None)
            if actual_value == expected_value:
                self.stdout.write(self.style.SUCCESS(f'✅ {setting_name} = {actual_value}'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ {setting_name} should be {expected_value}, got {actual_value}'))
        
        # Check database configuration
        db_engine = settings.DATABASES['default']['ENGINE']
        if 'postgresql' in db_engine:
            self.stdout.write(self.style.SUCCESS('✅ PostgreSQL database configured'))
        elif 'sqlite' in db_engine and not settings.DEBUG:
            self.stdout.write(self.style.WARNING('⚠️ SQLite should not be used in production'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✅ Database engine: {db_engine}'))
        
        # Check static files
        if hasattr(settings, 'STATICFILES_STORAGE'):
            self.stdout.write(self.style.SUCCESS(f'✅ Static files storage: {settings.STATICFILES_STORAGE}'))
        
        self.stdout.write('\n📋 Production Readiness Summary:')
        self.stdout.write('- Set environment variables in production')
        self.stdout.write('- Run: python manage.py collectstatic')
        self.stdout.write('- Run: python manage.py migrate')
        self.stdout.write('- Configure SSL/HTTPS')
        self.stdout.write('- Set up monitoring and backups')