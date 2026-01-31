#!/usr/bin/env python3
"""
API testing script for GutSense backend
"""

import requests
import json
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

class APITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.user_id = None
    
    def test_health(self) -> bool:
        """Test health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                print("✅ Health check passed")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to server. Is it running?")
            return False
    
    def test_signup(self) -> bool:
        """Test user signup"""
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/auth/signup", json=data)
            if response.status_code == 201:
                result = response.json()
                self.token = result["access_token"]
                self.user_id = result["user"]["id"]
                print("✅ Signup successful")
                return True
            elif response.status_code == 400:
                # User might already exist, try login
                return self.test_login()
            else:
                print(f"❌ Signup failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Signup error: {e}")
            return False
    
    def test_login(self) -> bool:
        """Test user login"""
        data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/auth/login", json=data)
            if response.status_code == 200:
                result = response.json()
                self.token = result["access_token"]
                self.user_id = result["user"]["id"]
                print("✅ Login successful")
                return True
            else:
                print(f"❌ Login failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def get_headers(self) -> Dict[str, str]:
        """Get authorization headers"""
        return {"Authorization": f"Bearer {self.token}"}
    
    def test_gut_profile(self) -> bool:
        """Test gut profile creation"""
        data = {
            "gut_type": "balanced",
            "sensitivities": ["acidity", "lactose"],
            "spice_tolerance": 2,
            "additional_notes": "Test profile"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/gut-profile/",
                json=data,
                headers=self.get_headers()
            )
            if response.status_code in [200, 201]:
                print("✅ Gut profile created/updated")
                return True
            else:
                print(f"❌ Gut profile failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Gut profile error: {e}")
            return False
    
    def test_food_analysis(self) -> bool:
        """Test food analysis"""
        data = {
            "food_name": "Spicy Pizza",
            "food_category": "italian"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/food/analyze",
                json=data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Food analysis successful: {result['reaction']}")
                print(f"   Explanation: {result['explanation'][:100]}...")
                return True
            else:
                print(f"❌ Food analysis failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Food analysis error: {e}")
            return False
    
    def test_food_history(self) -> bool:
        """Test food history retrieval"""
        try:
            response = requests.get(
                f"{self.base_url}/api/food/history",
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Food history retrieved: {len(result)} items")
                return True
            else:
                print(f"❌ Food history failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Food history error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🧪 Running GutSense API Tests")
        print("=" * 40)
        
        tests = [
            ("Health Check", self.test_health),
            ("User Signup/Login", self.test_signup),
            ("Gut Profile", self.test_gut_profile),
            ("Food Analysis", self.test_food_analysis),
            ("Food History", self.test_food_history),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🔍 Testing {test_name}...")
            if test_func():
                passed += 1
            else:
                print(f"   Skipping remaining tests due to failure")
                break
        
        print(f"\n📊 Test Results: {passed}/{total} passed")
        
        if passed == total:
            print("🎉 All tests passed! API is working correctly.")
        else:
            print("❌ Some tests failed. Check the server logs.")
            sys.exit(1)

def main():
    """Main function"""
    tester = APITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()