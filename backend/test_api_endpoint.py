#!/usr/bin/env python
"""
Test the aws-health API endpoint directly
Run with: python test_api_endpoint.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.test import RequestFactory
from database.views import aws_station_health_logs
from django.http import HttpRequest

def test_api_endpoint():
    print("=== TESTING AWS-HEALTH API ENDPOINT ===\n")
    
    # Create a mock request
    factory = RequestFactory()
    
    # Test with OTT brand (which should now only show POS_SAT, SYNOP_SAT, TOCO_SAT)
    print("🔍 Testing OTT brand filter:")
    request = factory.get('/api/stations/aws-health/', {'brand': 'OTT'})
    response = aws_station_health_logs(request)
    
    if response.status_code == 200:
        data = response.data
        print(f"✅ API call successful")
        print(f"   Total stations: {data['pagination']['total']}")
        print(f"   Current page: {data['pagination']['page']}")
        print(f"   Page size: {data['pagination']['page_size']}")
        
        print(f"\n📊 Stations returned:")
        for station in data['data']:
            print(f"   • {station['name']}")
            print(f"     Status: {station['status']}")
            print(f"     Battery: {station['battery_status']}")
            print(f"     Connectivity: {station['connectivity_status']}")
            print(f"     Last Update: {station['created_at']}")
            print()
    else:
        print(f"❌ API call failed with status {response.status_code}")
        print(f"   Response: {response.data}")
    
    print("=" * 50)
    
    # Test with 3D_Paws brand (which should now include T14, T15, T16)
    print("🔍 Testing 3D_Paws brand filter:")
    request = factory.get('/api/stations/aws-health/', {'brand': '3D_Paws'})
    response = aws_station_health_logs(request)
    
    if response.status_code == 200:
        data = response.data
        print(f"✅ API call successful")
        print(f"   Total stations: {data['pagination']['total']}")
        print(f"   Current page: {data['pagination']['page']}")
        print(f"   Page size: {data['pagination']['page_size']}")
        
        print(f"\n📊 Stations returned:")
        for station in data['data']:
            print(f"   • {station['name']}")
            print(f"     Status: {station['status']}")
            print(f"     Battery: {station['battery_status']}")
            print(f"     Connectivity: {station['connectivity_status']}")
            print(f"     Last Update: {station['created_at']}")
            print()
    else:
        print(f"❌ API call failed with status {response.status_code}")
        print(f"   Response: {response.data}")
    
    print("=" * 50)
    
    # Test with no brand filter (all brands)
    print("🔍 Testing no brand filter (all brands):")
    request = factory.get('/api/stations/aws-health/')
    response = aws_station_health_logs(request)
    
    if response.status_code == 200:
        data = response.data
        print(f"✅ API call successful")
        print(f"   Total stations: {data['pagination']['total']}")
        print(f"   Current page: {data['pagination']['page']}")
        print(f"   Page size: {data['pagination']['page_size']}")
        
        print(f"\n📊 First 10 stations returned:")
        for i, station in enumerate(data['data'][:10]):
            print(f"   {i+1}. {station['name']} ({station['brand']})")
            print(f"      Status: {station['status']}")
            print(f"      Battery: {station['battery_status']}")
            print()
    else:
        print(f"❌ API call failed with status {response.status_code}")
        print(f"   Response: {response.data}")

if __name__ == "__main__":
    test_api_endpoint() 