#!/usr/bin/env python
"""
Security Testing Script for Django Application
This script performs basic security tests to verify implemented security measures.
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from bookshelf.models import Book
from bookshelf.forms import BookForm

User = get_user_model()

def test_csrf_protection():
    """Test CSRF protection on forms"""
    print("Testing CSRF Protection...")
    
    client = Client(enforce_csrf_checks=True)
    
    # Create a test user
    user = User.objects.create_user(username='testuser', password='testpass123')
    client.login(username='testuser', password='testpass123')
    
    # Try to submit form without CSRF token (should fail)
    response = client.post('/books/create/', {
        'title': 'Test Book',
        'author': 'Test Author',
        'publication_year': 2023
    })
    
    if response.status_code == 403:
        print("✓ CSRF protection working - form rejected without token")
    else:
        print("✗ CSRF protection may not be working properly")

def test_xss_prevention():
    """Test XSS prevention in forms"""
    print("Testing XSS Prevention...")
    
    # Test form validation with XSS attempt
    form_data = {
        'title': '<script>alert("XSS")</script>',
        'author': 'Test Author',
        'publication_year': 2023
    }
    
    form = BookForm(data=form_data)
    if form.is_valid():
        cleaned_title = form.cleaned_data['title']
        if '<script>' not in cleaned_title:
            print("✓ XSS prevention working - script tags removed")
        else:
            print("✗ XSS prevention may not be working")
    else:
        print("✓ Form validation rejected malicious input")

def test_sql_injection_prevention():
    """Test SQL injection prevention in search"""
    print("Testing SQL Injection Prevention...")
    
    client = Client()
    
    # Try SQL injection in search parameter
    response = client.get('/books/', {'search': "'; DROP TABLE bookshelf_book; --"})
    
    if response.status_code == 200:
        print("✓ SQL injection attempt handled safely")
    else:
        print("✗ Unexpected response to SQL injection attempt")

def test_input_validation():
    """Test input validation in forms"""
    print("Testing Input Validation...")
    
    # Test with invalid data
    invalid_data = [
        {'title': '', 'author': 'Test', 'publication_year': 2023},  # Empty title
        {'title': 'Test', 'author': '', 'publication_year': 2023},  # Empty author
        {'title': 'Test', 'author': 'Test', 'publication_year': 'invalid'},  # Invalid year
        {'title': 'Test', 'author': 'Test', 'publication_year': 999},  # Year too low
    ]
    
    valid_count = 0
    for data in invalid_data:
        form = BookForm(data=data)
        if not form.is_valid():
            valid_count += 1
    
    if valid_count == len(invalid_data):
        print("✓ Input validation working - all invalid data rejected")
    else:
        print(f"✗ Input validation issues - {len(invalid_data) - valid_count} invalid forms accepted")

def test_security_headers():
    """Test security headers in responses"""
    print("Testing Security Headers...")
    
    client = Client()
    response = client.get('/books/')
    
    security_headers = [
        'X-Frame-Options',
        'X-Content-Type-Options',
    ]
    
    headers_present = 0
    for header in security_headers:
        if header in response:
            headers_present += 1
            print(f"✓ {header} header present")
        else:
            print(f"✗ {header} header missing")
    
    if headers_present == len(security_headers):
        print("✓ All security headers present")
    else:
        print(f"✗ {len(security_headers) - headers_present} security headers missing")

def run_security_tests():
    """Run all security tests"""
    print("=" * 50)
    print("DJANGO SECURITY TESTING")
    print("=" * 50)
    
    try:
        test_csrf_protection()
        print()
        test_xss_prevention()
        print()
        test_sql_injection_prevention()
        print()
        test_input_validation()
        print()
        test_security_headers()
        print()
        
        print("=" * 50)
        print("SECURITY TESTING COMPLETED")
        print("=" * 50)
        print("Note: These are basic tests. Comprehensive security testing")
        print("should include professional security auditing tools.")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    run_security_tests()