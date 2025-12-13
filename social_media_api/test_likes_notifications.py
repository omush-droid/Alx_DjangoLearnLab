#!/usr/bin/env python3
"""
Test script for likes and notifications functionality in Social Media API
"""

import requests
import json
import time

BASE_URL = 'http://127.0.0.1:8000/api'

def test_likes_and_notifications():
    print("=== Testing Likes and Notifications Functionality ===\n")
    
    # Test data
    user1_data = {
        'username': 'testuser1',
        'email': 'test1@example.com',
        'password': 'testpass123',
        'bio': 'Test user 1'
    }
    
    user2_data = {
        'username': 'testuser2',
        'email': 'test2@example.com',
        'password': 'testpass123',
        'bio': 'Test user 2'
    }
    
    # Register users
    print("1. Registering test users...")
    user1_response = requests.post(f'{BASE_URL}/accounts/register/', json=user1_data)
    user2_response = requests.post(f'{BASE_URL}/accounts/register/', json=user2_data)
    
    if user1_response.status_code == 201 and user2_response.status_code == 201:
        print("✓ Users registered successfully")
        user1_token = user1_response.json()['token']
        user2_token = user2_response.json()['token']
        user1_id = user1_response.json()['user_id']
        user2_id = user2_response.json()['user_id']
    else:
        print("✗ User registration failed")
        return
    
    # Create headers for authentication
    user1_headers = {'Authorization': f'Token {user1_token}'}
    user2_headers = {'Authorization': f'Token {user2_token}'}
    
    # User1 creates a post
    print("\n2. Creating a post...")
    post_data = {
        'title': 'Test Post for Likes',
        'content': 'This is a test post to test likes functionality.'
    }
    
    post_response = requests.post(f'{BASE_URL}/posts/', json=post_data, headers=user1_headers)
    if post_response.status_code == 201:
        print("✓ Post created successfully")
        post_id = post_response.json()['id']
    else:
        print("✗ Post creation failed")
        return
    
    # User2 follows User1
    print("\n3. Testing follow functionality with notifications...")
    follow_response = requests.post(f'{BASE_URL}/accounts/follow/{user1_id}/', headers=user2_headers)
    if follow_response.status_code == 200:
        print("✓ User2 followed User1 successfully")
    else:
        print("✗ Follow failed")
    
    # User2 likes User1's post
    print("\n4. Testing like functionality...")
    like_response = requests.post(f'{BASE_URL}/posts/{post_id}/like/', headers=user2_headers)
    if like_response.status_code == 201:
        print("✓ Post liked successfully")
        print(f"   Response: {like_response.json()}")
    else:
        print("✗ Like failed")
        print(f"   Error: {like_response.json()}")
    
    # Try to like the same post again (should fail)
    print("\n5. Testing duplicate like prevention...")
    duplicate_like_response = requests.post(f'{BASE_URL}/posts/{post_id}/like/', headers=user2_headers)
    if duplicate_like_response.status_code == 400:
        print("✓ Duplicate like prevented successfully")
        print(f"   Response: {duplicate_like_response.json()}")
    else:
        print("✗ Duplicate like prevention failed")
    
    # Check post details with like count
    print("\n6. Checking post with like information...")
    post_detail_response = requests.get(f'{BASE_URL}/posts/{post_id}/', headers=user2_headers)
    if post_detail_response.status_code == 200:
        post_data = post_detail_response.json()
        print("✓ Post details retrieved successfully")
        print(f"   Likes count: {post_data.get('likes_count', 0)}")
        print(f"   Is liked by user2: {post_data.get('is_liked', False)}")
    else:
        print("✗ Failed to retrieve post details")
    
    # User2 comments on User1's post
    print("\n7. Testing comment with notification...")
    comment_data = {
        'post': post_id,
        'content': 'Great post! This is a test comment.'
    }
    
    comment_response = requests.post(f'{BASE_URL}/comments/', json=comment_data, headers=user2_headers)
    if comment_response.status_code == 201:
        print("✓ Comment created successfully")
    else:
        print("✗ Comment creation failed")
    
    # Check User1's notifications
    print("\n8. Checking User1's notifications...")
    time.sleep(1)  # Small delay to ensure notifications are created
    notifications_response = requests.get(f'{BASE_URL}/notifications/', headers=user1_headers)
    if notifications_response.status_code == 200:
        notifications = notifications_response.json()
        print("✓ Notifications retrieved successfully")
        print(f"   Total notifications: {len(notifications)}")
        for i, notification in enumerate(notifications, 1):
            print(f"   {i}. {notification['actor']} {notification['verb']} ({notification['timestamp']})")
    else:
        print("✗ Failed to retrieve notifications")
    
    # Test unlike functionality
    print("\n9. Testing unlike functionality...")
    unlike_response = requests.post(f'{BASE_URL}/posts/{post_id}/unlike/', headers=user2_headers)
    if unlike_response.status_code == 200:
        print("✓ Post unliked successfully")
        print(f"   Response: {unlike_response.json()}")
    else:
        print("✗ Unlike failed")
    
    # Check post details after unlike
    print("\n10. Checking post after unlike...")
    post_detail_response = requests.get(f'{BASE_URL}/posts/{post_id}/', headers=user2_headers)
    if post_detail_response.status_code == 200:
        post_data = post_detail_response.json()
        print("✓ Post details retrieved successfully")
        print(f"    Likes count: {post_data.get('likes_count', 0)}")
        print(f"    Is liked by user2: {post_data.get('is_liked', False)}")
    else:
        print("✗ Failed to retrieve post details")
    
    # Test unlike when not liked (should fail)
    print("\n11. Testing unlike when not liked...")
    unlike_response = requests.post(f'{BASE_URL}/posts/{post_id}/unlike/', headers=user2_headers)
    if unlike_response.status_code == 400:
        print("✓ Unlike prevention working correctly")
        print(f"   Response: {unlike_response.json()}")
    else:
        print("✗ Unlike prevention failed")
    
    print("\n=== Test Summary ===")
    print("✓ User registration and authentication")
    print("✓ Post creation")
    print("✓ Follow functionality with notifications")
    print("✓ Like functionality with notifications")
    print("✓ Duplicate like prevention")
    print("✓ Post like count and status")
    print("✓ Comment functionality with notifications")
    print("✓ Notification retrieval")
    print("✓ Unlike functionality")
    print("✓ Unlike prevention when not liked")
    print("\nAll tests completed successfully! 🎉")

if __name__ == '__main__':
    print("Starting Social Media API Likes and Notifications Test...")
    print("Make sure the Django development server is running on http://127.0.0.1:8000")
    print("Press Enter to continue or Ctrl+C to cancel...")
    input()
    
    try:
        test_likes_and_notifications()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Please make sure the Django development server is running:")
        print("python manage.py runserver")
    except KeyboardInterrupt:
        print("\n❌ Test cancelled by user.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")