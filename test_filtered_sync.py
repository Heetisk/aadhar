import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_filtered_sync():
    print("=" * 60)
    print("Testing Filtered API Sync")
    print("=" * 60)
    
    # Test 1: Fetch data for a specific state
    print("\n1. Fetching data for Gujarat...")
    r = requests.post(f"{BASE_URL}/sync-api?limit=50&state=Gujarat")
    print(f"Response: {r.status_code}")
    print(f"Message: {r.json()}")
    
    # Test 2: Fetch data for a specific district
    print("\n2. Fetching data for Surat district...")
    r = requests.post(f"{BASE_URL}/sync-api?limit=50&district=Surat")
    print(f"Response: {r.status_code}")
    print(f"Message: {r.json()}")
    
    # Test 3: Fetch data for both state and district
    print("\n3. Fetching data for Bhavnagar district in Gujarat...")
    r = requests.post(f"{BASE_URL}/sync-api?limit=50&state=Gujarat&district=Bhavnagar")
    print(f"Response: {r.status_code}")
    print(f"Message: {r.json()}")
    
    # Test 4: Check summary after all syncs
    print("\n4. Checking summary...")
    r = requests.get(f"{BASE_URL}/summary")
    print(f"Summary: {r.json()}")
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_filtered_sync()
