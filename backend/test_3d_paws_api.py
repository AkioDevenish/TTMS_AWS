#!/usr/bin/env python
"""
Test 3D Paws API directly to see if it's working
Run with: python test_3d_paws_api.py
"""

import requests
import json
from datetime import datetime, timedelta

def test_3d_paws_api():
    print("=== TESTING 3D PAWS API ===\n")
    
    # API configuration from data_fetcher.py
    portal_url = "http://3d-trinidad.icdp.ucar.edu"
    user_email = "jerome.ramirez@metoffice.gov.tt"
    api_key = "sVALwcRMyQmjtwYpDPW-"
    
    # Test time range (last 24 hours)
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)
    
    # Convert to Unix timestamps
    start_timestamp = int(start_time.timestamp())
    end_timestamp = int(end_time.timestamp())
    
    print(f"Testing API for time range: {start_time} to {end_time}")
    print(f"Start timestamp: {start_timestamp}")
    print(f"End timestamp: {end_timestamp}")
    
    # Test with a known working station (T10 Paramin - serial 2)
    test_station_serial = "2"
    
    print(f"\nTesting with station serial: {test_station_serial}")
    
    # Prepare request
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    params = {
        "from_time": start_timestamp,
        "to_time": end_timestamp
    }
    
    form_data = {
        "devices": (None, f'["{test_station_serial}"]')
    }
    
    try:
        print(f"Making request to: {portal_url}/api/historical_data")
        print(f"Headers: {headers}")
        print(f"Params: {params}")
        print(f"Form data: {form_data}")
        
        response = requests.post(
            f"{portal_url}/api/historical_data",
            headers=headers,
            params=params,
            files=form_data,
            timeout=30
        )
        
        print(f"\nResponse status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Response data type: {type(data)}")
                print(f"Response data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                
                if isinstance(data, dict):
                    features = data.get("features", [])
                    print(f"Number of features: {len(features)}")
                    
                    if features:
                        properties = features[0].get("properties", {})
                        data_entries = properties.get("data", [])
                        print(f"Number of data entries: {len(data_entries)}")
                        
                        if data_entries:
                            print(f"Sample data entry: {data_entries[0]}")
                        else:
                            print("No data entries found")
                    else:
                        print("No features found")
                else:
                    print(f"Raw response: {str(data)[:500]}...")
                    
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e}")
                print(f"Raw response: {response.text[:500]}...")
        else:
            print(f"API request failed with status {response.status_code}")
            print(f"Response text: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    
    # Test with a non-working station (T01 Rawinsonde - serial 1)
    print(f"\n{'='*50}")
    print(f"Testing with non-working station serial: 1")
    
    form_data = {
        "devices": (None, '["1"]')
    }
    
    try:
        response = requests.post(
            f"{portal_url}/api/historical_data",
            headers=headers,
            params=params,
            files=form_data,
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, dict):
                    features = data.get("features", [])
                    print(f"Number of features: {len(features)}")
                    
                    if features:
                        properties = features[0].get("properties", {})
                        data_entries = properties.get("data", [])
                        print(f"Number of data entries: {len(data_entries)}")
                    else:
                        print("No features found - station might not exist or have data")
                else:
                    print(f"Raw response: {str(data)[:500]}...")
                    
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e}")
        else:
            print(f"API request failed with status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_3d_paws_api() 