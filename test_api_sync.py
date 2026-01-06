import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_sync():
    print("Triggering API Sync...")
    try:
        # Limit to 10 for quick testing
        r = requests.post(f"{BASE_URL}/sync-api?limit=10&offset=0")
        print("Sync Response:", r.status_code, r.json())
        
        if r.status_code == 200:
            # Check summary to see if data increased
            r_summary = requests.get(f"{BASE_URL}/summary")
            print("Post-Sync Summary:", r_summary.json())
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_sync()
