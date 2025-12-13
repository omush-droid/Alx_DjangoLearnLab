#!/usr/bin/env python3
"""
Deployment Status Dashboard
Monitors the health and status of deployed Social Media API
"""

import requests
import time
import sys
from datetime import datetime
import json

class DeploymentMonitor:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.timeout = 10
        
    def check_endpoint(self, endpoint, expected_status=200):
        """Check if an endpoint is responding correctly"""
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}{endpoint}")
            response_time = (time.time() - start_time) * 1000
            
            return {
                'status': 'UP' if response.status_code == expected_status else 'DOWN',
                'status_code': response.status_code,
                'response_time': round(response_time, 2),
                'error': None
            }
        except requests.exceptions.RequestException as e:
            return {
                'status': 'DOWN',
                'status_code': None,
                'response_time': None,
                'error': str(e)
            }
    
    def get_system_info(self):
        """Get system information from health endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/health/")
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def generate_report(self):
        """Generate a comprehensive status report"""
        print(f"🔍 Social Media API Deployment Status")
        print(f"🌐 URL: {self.base_url}")
        print(f"⏰ Checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Check critical endpoints
        endpoints = [
            ('/', 'API Root'),
            ('/health/', 'Health Check'),
            ('/api/accounts/register/', 'User Registration'),
            ('/api/posts/', 'Posts API'),
            ('/api/comments/', 'Comments API'),
            ('/api/notifications/', 'Notifications API'),
            ('/admin/', 'Admin Panel'),
        ]
        
        all_up = True
        total_response_time = 0
        successful_checks = 0
        
        for endpoint, name in endpoints:
            result = self.check_endpoint(endpoint)
            status_icon = "✅" if result['status'] == 'UP' else "❌"
            
            print(f"{status_icon} {name:<20} | Status: {result['status']:<4} | "
                  f"Code: {result['status_code'] or 'N/A':<3} | "
                  f"Time: {result['response_time'] or 'N/A'}ms")
            
            if result['error']:
                print(f"   Error: {result['error']}")
            
            if result['status'] == 'DOWN':
                all_up = False
            else:
                if result['response_time']:
                    total_response_time += result['response_time']
                    successful_checks += 1
        
        print("-" * 60)
        
        # System information
        system_info = self.get_system_info()
        if system_info:
            print(f"📊 System Info:")
            print(f"   Version: {system_info.get('version', 'Unknown')}")
            print(f"   Debug Mode: {system_info.get('debug', 'Unknown')}")
        
        # Performance metrics
        if successful_checks > 0:
            avg_response_time = total_response_time / successful_checks
            print(f"⚡ Performance:")
            print(f"   Average Response Time: {avg_response_time:.2f}ms")
            
            if avg_response_time < 200:
                print("   🟢 Excellent performance")
            elif avg_response_time < 500:
                print("   🟡 Good performance")
            else:
                print("   🔴 Slow performance - consider optimization")
        
        # Overall status
        print("-" * 60)
        if all_up:
            print("🎉 Overall Status: ALL SYSTEMS OPERATIONAL")
        else:
            print("⚠️ Overall Status: SOME ISSUES DETECTED")
        
        return all_up
    
    def continuous_monitoring(self, interval=60):
        """Run continuous monitoring"""
        print(f"🔄 Starting continuous monitoring (checking every {interval}s)")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                self.generate_report()
                print(f"\n⏳ Next check in {interval} seconds...\n")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped by user")

def main():
    if len(sys.argv) < 2:
        print("Usage: python deployment_status.py <base_url> [--monitor]")
        print("Example: python deployment_status.py https://your-app.herokuapp.com")
        print("         python deployment_status.py https://your-app.herokuapp.com --monitor")
        sys.exit(1)
    
    base_url = sys.argv[1]
    monitor_mode = '--monitor' in sys.argv
    
    monitor = DeploymentMonitor(base_url)
    
    if monitor_mode:
        monitor.continuous_monitoring()
    else:
        success = monitor.generate_report()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()