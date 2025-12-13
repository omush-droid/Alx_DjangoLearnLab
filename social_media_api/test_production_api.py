#!/usr/bin/env python3
"""
Production API Testing Script for Social Media API
Tests all endpoints to ensure proper deployment
"""

import requests
import json
import sys
from urllib.parse import urljoin

class ProductionAPITester:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.token = None
        self.user_id = None
        
    def test_health_check(self):
        """Test health check endpoint"""
        print("🔍 Testing health check...")
        try:
            response = self.session.get(f"{self.base_url}/health/")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_api_root(self):
        """Test API root endpoint"""
        print("🔍 Testing API root...")
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API root accessible: {data['message']}")
                return True
            else:
                print(f"❌ API root failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ API root error: {e}")
            return False
    
    def test_user_registration(self):
        """Test user registration"""
        print("🔍 Testing user registration...")
        try:
            user_data = {
                "username": "testuser_prod",
                "email": "test@production.com",
                "password": "testpass123",
                "bio": "Production test user"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/accounts/register/",
                json=user_data
            )
            
            if response.status_code == 201:
                data = response.json()
                self.token = data.get('token')
                self.user_id = data.get('user_id')
                print(f"✅ User registration successful: {data['username']}")
                
                # Set authorization header for future requests
                self.session.headers.update({'Authorization': f'Token {self.token}'})
                return True
            else:
                print(f"❌ User registration failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ User registration error: {e}")
            return False
    
    def test_user_profile(self):
        """Test user profile access"""
        print("🔍 Testing user profile...")
        try:
            response = self.session.get(f"{self.base_url}/api/accounts/profile/")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Profile access successful: {data['username']}")
                return True
            else:
                print(f"❌ Profile access failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Profile access error: {e}")
            return False
    
    def test_post_creation(self):
        """Test post creation"""
        print("🔍 Testing post creation...")
        try:
            post_data = {
                "title": "Production Test Post",
                "content": "This is a test post created during production testing."
            }
            
            response = self.session.post(
                f"{self.base_url}/api/posts/",
                json=post_data
            )
            
            if response.status_code == 201:
                data = response.json()
                self.post_id = data.get('id')
                print(f"✅ Post creation successful: {data['title']}")
                return True
            else:
                print(f"❌ Post creation failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Post creation error: {e}")
            return False
    
    def test_posts_list(self):
        """Test posts listing"""
        print("🔍 Testing posts listing...")
        try:
            response = self.session.get(f"{self.base_url}/api/posts/")
            
            if response.status_code == 200:
                data = response.json()
                posts_count = len(data.get('results', []))
                print(f"✅ Posts listing successful: {posts_count} posts found")
                return True
            else:
                print(f"❌ Posts listing failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Posts listing error: {e}")
            return False
    
    def test_comment_creation(self):
        """Test comment creation"""
        print("🔍 Testing comment creation...")
        try:
            if not hasattr(self, 'post_id'):
                print("⚠️ Skipping comment test - no post available")
                return True
                
            comment_data = {
                "post": self.post_id,
                "content": "This is a test comment for production testing."
            }
            
            response = self.session.post(
                f"{self.base_url}/api/comments/",
                json=comment_data
            )
            
            if response.status_code == 201:
                data = response.json()
                print(f"✅ Comment creation successful: {data['content'][:50]}...")
                return True
            else:
                print(f"❌ Comment creation failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Comment creation error: {e}")
            return False
    
    def test_notifications(self):
        """Test notifications endpoint"""
        print("🔍 Testing notifications...")
        try:
            response = self.session.get(f"{self.base_url}/api/notifications/")
            
            if response.status_code == 200:
                data = response.json()
                notifications_count = len(data)
                print(f"✅ Notifications access successful: {notifications_count} notifications")
                return True
            else:
                print(f"❌ Notifications access failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Notifications access error: {e}")
            return False
    
    def test_feed(self):
        """Test feed endpoint"""
        print("🔍 Testing feed...")
        try:
            response = self.session.get(f"{self.base_url}/api/feed/")
            
            if response.status_code == 200:
                data = response.json()
                feed_count = len(data)
                print(f"✅ Feed access successful: {feed_count} posts in feed")
                return True
            else:
                print(f"❌ Feed access failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Feed access error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all production tests"""
        print(f"🚀 Starting production API tests for: {self.base_url}")
        print("=" * 60)
        
        tests = [
            self.test_health_check,
            self.test_api_root,
            self.test_user_registration,
            self.test_user_profile,
            self.test_post_creation,
            self.test_posts_list,
            self.test_comment_creation,
            self.test_notifications,
            self.test_feed,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ Test {test.__name__} crashed: {e}")
                failed += 1
            print("-" * 40)
        
        print(f"\n📊 Test Results:")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
        
        if failed == 0:
            print("🎉 All tests passed! Your API is ready for production.")
            return True
        else:
            print("⚠️ Some tests failed. Please check the issues above.")
            return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_production_api.py <base_url>")
        print("Example: python test_production_api.py https://your-app.herokuapp.com")
        sys.exit(1)
    
    base_url = sys.argv[1]
    tester = ProductionAPITester(base_url)
    
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()