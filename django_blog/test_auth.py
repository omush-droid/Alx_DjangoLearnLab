#!/usr/bin/env python
"""
Test script for Django Blog Authentication System
Run this after starting the development server to test authentication features.
"""

import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

def test_authentication_system():
    """Test the authentication system functionality"""
    client = Client()
    
    print("Testing Django Blog Authentication System")
    print("=" * 50)
    
    # Test 1: Home page access
    response = client.get('/')
    print(f"[OK] Home page accessible: {response.status_code == 200}")
    
    # Test 2: Registration page access
    response = client.get('/register/')
    print(f"[OK] Registration page accessible: {response.status_code == 200}")
    
    # Test 3: Login page access
    response = client.get('/login/')
    print(f"[OK] Login page accessible: {response.status_code == 200}")
    
    # Test 4: Profile page requires login
    response = client.get('/profile/')
    print(f"[OK] Profile page requires login: {response.status_code == 302}")
    
    # Test 5: Create test user
    try:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        print("[OK] Test user created successfully")
    except:
        print("[WARN] Test user already exists or creation failed")
    
    # Test 6: Login functionality
    login_success = client.login(username='testuser', password='testpass123')
    print(f"[OK] User login successful: {login_success}")
    
    # Test 7: Profile page access after login
    if login_success:
        response = client.get('/profile/')
        print(f"[OK] Profile page accessible after login: {response.status_code == 200}")
    
    print("\nAuthentication system tests completed!")
    print("Start the server with: python manage.py runserver")
    print("Then visit: http://127.0.0.1:8000/")

if __name__ == '__main__':
    test_authentication_system()