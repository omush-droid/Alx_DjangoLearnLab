#!/usr/bin/env python
"""
Test script for Social Media API Follow and Feed functionality.
Tests follow/unfollow operations and feed generation.
"""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api"

class FollowFeedTester:
    def __init__(self):
        self.session = requests.Session()
        self.users = {}  # Store user data
        
    def register_user(self, username, email, password):
        """Register a new user and return user data"""
        data = {
            "username": username,
            "email": email,
            "password": password,
            "bio": f"Bio for {username}"
        }
        response = self.session.post(f"{BASE_URL}/accounts/register/", json=data)
        if response.status_code == 201:
            result = response.json()
            user_data = {
                'token': result.get('token'),
                'user_id': result.get('user_id'),
                'username': result.get('username')
            }
            self.users[username] = user_data
            print(f"✓ User registered: {username} (ID: {user_data['user_id']})")
            return user_data
        else:
            print(f"✗ Registration failed for {username}: {response.text}")
            return None
    
    def follow_user(self, follower_username, target_user_id):
        """Follow a user"""
        follower = self.users[follower_username]
        headers = {'Authorization': f'Token {follower["token"]}'}
        
        response = requests.post(f"{BASE_URL}/accounts/follow/{target_user_id}/", headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ {follower_username} followed user {target_user_id}: {result['message']}")
            return True
        else:
            print(f"✗ Follow failed: {response.text}")
            return False
    
    def unfollow_user(self, follower_username, target_user_id):
        """Unfollow a user"""
        follower = self.users[follower_username]
        headers = {'Authorization': f'Token {follower["token"]}'}
        
        response = requests.post(f"{BASE_URL}/accounts/unfollow/{target_user_id}/", headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ {follower_username} unfollowed user {target_user_id}: {result['message']}")
            return True
        else:
            print(f"✗ Unfollow failed: {response.text}")
            return False
    
    def create_post(self, username, title, content):
        """Create a post as a specific user"""
        user = self.users[username]
        headers = {'Authorization': f'Token {user["token"]}'}
        data = {"title": title, "content": content}
        
        response = requests.post(f"{BASE_URL}/posts/", json=data, headers=headers)
        if response.status_code == 201:
            result = response.json()
            print(f"✓ Post created by {username}: '{result['title']}' (ID: {result['id']})")
            return result['id']
        else:
            print(f"✗ Post creation failed: {response.text}")
            return None
    
    def get_feed(self, username):
        """Get feed for a specific user"""
        user = self.users[username]
        headers = {'Authorization': f'Token {user["token"]}'}
        
        response = requests.get(f"{BASE_URL}/feed/", headers=headers)
        if response.status_code == 200:
            posts = response.json()
            print(f"✓ Feed retrieved for {username}: {len(posts)} posts")
            return posts
        else:
            print(f"✗ Feed retrieval failed: {response.text}")
            return None
    
    def get_profile(self, username):
        """Get user profile"""
        user = self.users[username]
        headers = {'Authorization': f'Token {user["token"]}'}
        
        response = requests.get(f"{BASE_URL}/accounts/profile/", headers=headers)
        if response.status_code == 200:
            profile = response.json()
            print(f"✓ Profile retrieved for {username}: following {len(profile.get('followers', []))} users")
            return profile
        else:
            print(f"✗ Profile retrieval failed: {response.text}")
            return None

def run_follow_feed_tests():
    """Run comprehensive tests for follow and feed functionality"""
    print("🚀 Starting Follow and Feed Tests")
    print("=" * 50)
    
    tester = FollowFeedTester()
    
    # Test 1: Register multiple users
    print("\n👥 Test 1: User Registration")
    user1 = tester.register_user("alice", "alice@example.com", "testpass123")
    user2 = tester.register_user("bob", "bob@example.com", "testpass123")
    user3 = tester.register_user("charlie", "charlie@example.com", "testpass123")
    
    if not all([user1, user2, user3]):
        print("❌ Test failed: User registration")
        return False
    
    # Test 2: Create posts by different users
    print("\n📝 Test 2: Create Posts")
    post1 = tester.create_post("alice", "Alice's First Post", "Hello from Alice!")
    post2 = tester.create_post("bob", "Bob's Adventure", "Bob's exciting day out")
    post3 = tester.create_post("charlie", "Charlie's Thoughts", "Some deep thoughts by Charlie")
    
    if not all([post1, post2, post3]):
        print("❌ Test failed: Post creation")
        return False
    
    # Test 3: Follow functionality
    print("\n👥 Test 3: Follow Operations")
    # Alice follows Bob and Charlie
    follow1 = tester.follow_user("alice", user2['user_id'])
    follow2 = tester.follow_user("alice", user3['user_id'])
    
    # Bob follows Charlie
    follow3 = tester.follow_user("bob", user3['user_id'])
    
    if not all([follow1, follow2, follow3]):
        print("❌ Test failed: Follow operations")
        return False
    
    # Test 4: Check profiles to verify follows
    print("\n👤 Test 4: Profile Verification")
    alice_profile = tester.get_profile("alice")
    if not alice_profile:
        print("❌ Test failed: Profile retrieval")
        return False
    
    # Test 5: Feed functionality
    print("\n📰 Test 5: Feed Generation")
    alice_feed = tester.get_feed("alice")  # Should see posts from Bob and Charlie
    bob_feed = tester.get_feed("bob")      # Should see posts from Charlie
    charlie_feed = tester.get_feed("charlie")  # Should see no posts (follows nobody)
    
    if alice_feed is None or bob_feed is None or charlie_feed is None:
        print("❌ Test failed: Feed retrieval")
        return False
    
    # Verify feed contents
    print(f"  - Alice's feed has {len(alice_feed)} posts (expected: 2)")
    print(f"  - Bob's feed has {len(bob_feed)} posts (expected: 1)")
    print(f"  - Charlie's feed has {len(charlie_feed)} posts (expected: 0)")
    
    # Test 6: Unfollow functionality
    print("\n👋 Test 6: Unfollow Operations")
    unfollow1 = tester.unfollow_user("alice", user2['user_id'])  # Alice unfollows Bob
    
    if not unfollow1:
        print("❌ Test failed: Unfollow operation")
        return False
    
    # Test 7: Verify feed after unfollow
    print("\n📰 Test 7: Feed After Unfollow")
    alice_feed_after = tester.get_feed("alice")  # Should now see only Charlie's posts
    
    if alice_feed_after is None:
        print("❌ Test failed: Feed after unfollow")
        return False
    
    print(f"  - Alice's feed after unfollowing Bob: {len(alice_feed_after)} posts (expected: 1)")
    
    # Test 8: Try to follow self (should fail)
    print("\n🚫 Test 8: Self-Follow Prevention")
    self_follow = tester.follow_user("alice", user1['user_id'])
    if self_follow:
        print("❌ Test failed: Self-follow should be prevented")
        return False
    else:
        print("✓ Self-follow correctly prevented")
    
    print("\n🎉 All follow and feed tests passed successfully!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    print("Make sure the Django development server is running on http://127.0.0.1:8000")
    print("Run: python manage.py runserver")
    input("Press Enter to continue with tests...")
    
    success = run_follow_feed_tests()
    sys.exit(0 if success else 1)