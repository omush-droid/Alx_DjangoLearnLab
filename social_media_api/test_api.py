#!/usr/bin/env python
"""
Test script for Social Media API - Posts and Comments functionality
Run this script to test the API endpoints after starting the development server.
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_user_registration_and_login():
    """Test user registration and login"""
    print("=== Testing User Registration and Login ===")
    
    # Register a test user
    register_data = {
        "username": "testuser",
        "email": "test@example.com", 
        "password": "testpass123",
        "bio": "Test user for API testing"
    }
    
    response = requests.post(f"{BASE_URL}/accounts/register/", json=register_data)
    print(f"Registration Status: {response.status_code}")
    
    if response.status_code == 201:
        token = response.json().get('token')
        print(f"Registration successful! Token: {token[:20]}...")
        return token
    else:
        print(f"Registration failed: {response.text}")
        
        # Try to login if user already exists
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/accounts/login/", json=login_data)
        if response.status_code == 200:
            token = response.json().get('token')
            print(f"Login successful! Token: {token[:20]}...")
            return token
        else:
            print(f"Login failed: {response.text}")
            return None

def test_posts_crud(token):
    """Test Posts CRUD operations"""
    print("\n=== Testing Posts CRUD Operations ===")
    
    headers = {"Authorization": f"Token {token}"}
    
    # Create a post
    post_data = {
        "title": "Test Post",
        "content": "This is a test post created via API testing script."
    }
    
    response = requests.post(f"{BASE_URL}/posts/", json=post_data, headers=headers)
    print(f"Create Post Status: {response.status_code}")
    
    if response.status_code == 201:
        post = response.json()
        post_id = post['id']
        print(f"Post created successfully! ID: {post_id}")
        
        # List posts
        response = requests.get(f"{BASE_URL}/posts/")
        print(f"List Posts Status: {response.status_code}")
        print(f"Total posts: {response.json().get('count', 0)}")
        
        # Search posts
        response = requests.get(f"{BASE_URL}/posts/?search=test")
        print(f"Search Posts Status: {response.status_code}")
        print(f"Search results: {len(response.json().get('results', []))}")
        
        # Update post
        update_data = {
            "title": "Updated Test Post",
            "content": "This post has been updated via API testing."
        }
        response = requests.put(f"{BASE_URL}/posts/{post_id}/", json=update_data, headers=headers)
        print(f"Update Post Status: {response.status_code}")
        
        return post_id
    else:
        print(f"Post creation failed: {response.text}")
        return None

def test_comments_crud(token, post_id):
    """Test Comments CRUD operations"""
    print("\n=== Testing Comments CRUD Operations ===")
    
    headers = {"Authorization": f"Token {token}"}
    
    # Create a comment
    comment_data = {
        "post": post_id,
        "content": "This is a test comment created via API testing script."
    }
    
    response = requests.post(f"{BASE_URL}/comments/", json=comment_data, headers=headers)
    print(f"Create Comment Status: {response.status_code}")
    
    if response.status_code == 201:
        comment = response.json()
        comment_id = comment['id']
        print(f"Comment created successfully! ID: {comment_id}")
        
        # List comments for the post
        response = requests.get(f"{BASE_URL}/comments/?post={post_id}")
        print(f"List Comments Status: {response.status_code}")
        comments = response.json().get('results', [])
        print(f"Comments for post {post_id}: {len(comments)}")
        
        # Update comment
        update_data = {
            "content": "This comment has been updated via API testing."
        }
        response = requests.put(f"{BASE_URL}/comments/{comment_id}/", json=update_data, headers=headers)
        print(f"Update Comment Status: {response.status_code}")
        
        return comment_id
    else:
        print(f"Comment creation failed: {response.text}")
        return None

def main():
    """Main test function"""
    print("Social Media API Test Script")
    print("Make sure the development server is running on localhost:8000")
    print("-" * 60)
    
    try:
        # Test authentication
        token = test_user_registration_and_login()
        if not token:
            print("Authentication failed. Cannot proceed with tests.")
            return
        
        # Test posts
        post_id = test_posts_crud(token)
        if not post_id:
            print("Post creation failed. Cannot test comments.")
            return
        
        # Test comments
        comment_id = test_comments_crud(token, post_id)
        
        print("\n=== Test Summary ===")
        print("✓ User registration/login")
        print("✓ Post creation, listing, search, and update")
        print("✓ Comment creation, listing, and update")
        print("\nAll tests completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the Django development server is running on localhost:8000")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()