#!/usr/bin/env python
"""
Test the aws-health API endpoint with larger page size
Run with: python test_large_page.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.test import RequestFactory
from database.views import aws_station_health_logs

def test_large_page():
    print("=== TESTING AWS-HEALTH API WITH LARGE PAGE SIZE ===\n")
    
    # Create a mock request
    factory = RequestFactory()
    
    # Test 3D_Paws brand with page size 50 (should show all 20 stations)
    print("🔍 Testing 3D_Paws brand with page size 50:")
    request = factory.get('/api/stations/aws-health/', {'brand': '3D_Paws', 'page_size': 50})
    response = aws_station_health_logs(request)
    
    if response.status_code == 200:
        data = response.data
        print(f"✅ API call successful")
        print(f"   Total stations: {data['pagination']['total']}")
        print(f"   Current page: {data['pagination']['page']}")
        print(f"   Page size: {data['pagination']['page_size']}")
        print(f"   Total pages: {data['pagination']['total_pages']}")
        print(f"   Has next: {data['pagination']['has_next']}")
        
        print(f"\n📊 All stations returned ({len(data['data'])} total):")
        for i, station in enumerate(data['data'], 1):
            print(f"   {i:2d}. {station['name']}")
            print(f"       Status: {station['status']}")
            print(f"       Battery: {station['battery_status']}")
            print(f"       Connectivity: {station['connectivity_status']}")
            print()
        
        # Check if T14, T15, T16 are included
        station_names = [s['name'] for s in data['data']]
        target_stations = ['T14 UTT', 'T15 ASJA', 'T16 Lochmaben']
        
        print("🎯 Checking for target stations:")
        for target in target_stations:
            if target in station_names:
                print(f"   ✅ {target} - FOUND")
            else:
                print(f"   ❌ {target} - NOT FOUND")
        
    else:
        print(f"❌ API call failed with status {response.status_code}")
        print(f"   Response: {response.data}")

if __name__ == "__main__":
    test_large_page() 