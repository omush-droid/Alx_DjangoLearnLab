#!/usr/bin/env python
"""
Comprehensive test script for Social Media API Posts and Comments functionality.
Tests all CRUD operations, permissions, filtering, and pagination.
"""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api"
ACCOUNTS_URL = f"{BASE_URL}/accounts"

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_id = None
        self.username = None
        
    def register_user(self, username, email, password, bio="Test user bio"):
        """Register a new user"""
        data = {
            "username": username,
            "email": email,
            "password": password,
            "bio": bio
        }
        response = self.session.post(f"{ACCOUNTS_URL}/register/", json=data)
        if response.status_code == 201:
            result = response.json()
            self.token = result.get('token')
            self.user_id = result.get('user_id')
            self.username = result.get('username')
            self.session.headers.update({'Authorization': f'Token {self.token}'})
            print(f"✓ User registered: {username}")
            return True
        else:
            print(f"✗ Registration failed: {response.text}")
            return False
    
    def login_user(self, username, password):
        """Login existing user"""
        data = {"username": username, "password": password}
        response = self.session.post(f"{ACCOUNTS_URL}/login/", json=data)
        if response.status_code == 200:
            result = response.json()
            self.token = result.get('token')
            self.user_id = result.get('user_id')
            self.username = result.get('username')
            self.session.headers.update({'Authorization': f'Token {self.token}'})
            print(f"✓ User logged in: {username}")
            return True
        else:
            print(f"✗ Login failed: {response.text}")
            return False
    
    def create_post(self, title, content):
        """Create a new post"""
        data = {"title": title, "content": content}
        response = self.session.post(f"{BASE_URL}/posts/", json=data)
        if response.status_code == 201:
            result = response.json()
            print(f"✓ Post created: {result['title']} (ID: {result['id']})")
            return result['id']
        else:
            print(f"✗ Post creation failed: {response.text}")
            return None
    
    def list_posts(self, search=None, author=None, page=1):
        """List posts with optional filtering"""
        params = {"page": page}
        if search:
            params["search"] = search
        if author:
            params["author"] = author
            
        response = self.session.get(f"{BASE_URL}/posts/", params=params)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Posts listed: {result['count']} total posts")
            return result
        else:
            print(f"✗ Posts listing failed: {response.text}")
            return None
    
    def get_post(self, post_id):
        """Get a specific post"""
        response = self.session.get(f"{BASE_URL}/posts/{post_id}/")
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Post retrieved: {result['title']}")
            return result
        else:
            print(f"✗ Post retrieval failed: {response.text}")
            return None
    
    def update_post(self, post_id, title=None, content=None):
        """Update a post"""
        data = {}
        if title:
            data["title"] = title
        if content:
            data["content"] = content
            
        response = self.session.put(f"{BASE_URL}/posts/{post_id}/", json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Post updated: {result['title']}")
            return result
        else:
            print(f"✗ Post update failed: {response.text}")
            return None
    
    def delete_post(self, post_id):
        """Delete a post"""
        response = self.session.delete(f"{BASE_URL}/posts/{post_id}/")
        if response.status_code == 204:
            print(f"✓ Post deleted: ID {post_id}")
            return True
        else:
            print(f"✗ Post deletion failed: {response.text}")
            return False
    
    def create_comment(self, post_id, content):
        """Create a comment on a post"""
        data = {"post": post_id, "content": content}
        response = self.session.post(f"{BASE_URL}/comments/", json=data)
        if response.status_code == 201:
            result = response.json()
            print(f"✓ Comment created on post {post_id} (ID: {result['id']})")
            return result['id']
        else:
            print(f"✗ Comment creation failed: {response.text}")
            return None
    
    def list_comments(self, post_id=None, author=None):
        """List comments with optional filtering"""
        params = {}
        if post_id:
            params["post"] = post_id
        if author:
            params["author"] = author
            
        response = self.session.get(f"{BASE_URL}/comments/", params=params)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Comments listed: {result['count']} total comments")
            return result
        else:
            print(f"✗ Comments listing failed: {response.text}")
            return None
    
    def update_comment(self, comment_id, content):
        """Update a comment"""
        data = {"content": content}
        response = self.session.put(f"{BASE_URL}/comments/{comment_id}/", json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Comment updated: ID {comment_id}")
            return result
        else:
            print(f"✗ Comment update failed: {response.text}")
            return None
    
    def delete_comment(self, comment_id):
        """Delete a comment"""
        response = self.session.delete(f"{BASE_URL}/comments/{comment_id}/")
        if response.status_code == 204:
            print(f"✓ Comment deleted: ID {comment_id}")
            return True
        else:
            print(f"✗ Comment deletion failed: {response.text}")
            return False

def run_comprehensive_tests():
    """Run comprehensive tests for the Social Media API"""
    print("🚀 Starting Social Media API Tests")
    print("=" * 50)
    
    tester = APITester()
    
    # Test 1: User Registration and Authentication
    print("\n📝 Test 1: User Registration and Authentication")
    if not tester.register_user("testuser1", "test1@example.com", "testpass123"):
        print("❌ Test failed: User registration")
        return False
    
    # Test 2: Post Creation
    print("\n📄 Test 2: Post CRUD Operations")
    post_id = tester.create_post("My First Post", "This is the content of my first post.")
    if not post_id:
        print("❌ Test failed: Post creation")
        return False
    
    # Test 3: Post Listing and Retrieval
    posts = tester.list_posts()
    if not posts:
        print("❌ Test failed: Post listing")
        return False
    
    post = tester.get_post(post_id)
    if not post:
        print("❌ Test failed: Post retrieval")
        return False
    
    # Test 4: Post Update
    updated_post = tester.update_post(post_id, title="Updated Post Title", content="Updated content")
    if not updated_post:
        print("❌ Test failed: Post update")
        return False
    
    # Test 5: Comment Creation
    print("\n💬 Test 3: Comment CRUD Operations")
    comment_id = tester.create_comment(post_id, "Great post! Thanks for sharing.")
    if not comment_id:
        print("❌ Test failed: Comment creation")
        return False
    
    # Test 6: Comment Listing and Filtering
    comments = tester.list_comments(post_id=post_id)
    if not comments:
        print("❌ Test failed: Comment listing")
        return False
    
    # Test 7: Comment Update
    updated_comment = tester.update_comment(comment_id, "Updated comment content")
    if not updated_comment:
        print("❌ Test failed: Comment update")
        return False
    
    # Test 8: Search Functionality
    print("\n🔍 Test 4: Search and Filtering")
    search_results = tester.list_posts(search="Updated")
    if not search_results:
        print("❌ Test failed: Post search")
        return False
    
    # Test 9: Create second user for permission testing
    print("\n👥 Test 5: Permissions Testing")
    tester2 = APITester()
    if not tester2.register_user("testuser2", "test2@example.com", "testpass123"):
        print("❌ Test failed: Second user registration")
        return False
    
    # Test 10: Try to update another user's post (should fail)
    unauthorized_update = tester2.update_post(post_id, title="Unauthorized Update")
    if unauthorized_update:
        print("❌ Test failed: Unauthorized post update should be blocked")
        return False
    else:
        print("✓ Unauthorized post update correctly blocked")
    
    # Test 11: Cleanup - Delete comment and post
    print("\n🧹 Test 6: Cleanup Operations")
    if not tester.delete_comment(comment_id):
        print("❌ Test failed: Comment deletion")
        return False
    
    if not tester.delete_post(post_id):
        print("❌ Test failed: Post deletion")
        return False
    
    print("\n🎉 All tests passed successfully!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    print("Make sure the Django development server is running on http://127.0.0.1:8000")
    print("Run: python manage.py runserver")
    input("Press Enter to continue with tests...")
    
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)