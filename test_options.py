import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_options():
    print("Testing Options Endpoints...")
    
    # Test States
    print("\n1. Fetching States options...")
    r = requests.get(f"{BASE_URL}/options/states")
    print(f"Status: {r.status_code}")
    print(f"States: {r.json()}")
    
    # Test Districts (no filter)
    print("\n2. Fetching All Districts options...")
    r = requests.get(f"{BASE_URL}/options/districts")
    print(f"Status: {r.status_code}")
    districts = r.json()
    print(f"Districts Count: {len(districts)}")
    if len(districts) > 0:
        print(f"First 5: {districts[:5]}")
        
    # Test Districts (filter by state)
    if len(r.json()) > 0:
        # Pick a state existing in DB if possible, else pick random
        # First ensure we have data. If states list is empty, we can't test filtering effectively without syncing first.
        states = requests.get(f"{BASE_URL}/options/states").json()
        if states:
            test_state = states[0]
            print(f"\n3. Fetching Districts for state '{test_state}'...")
            r = requests.get(f"{BASE_URL}/options/districts?state={test_state}")
            print(f"Status: {r.status_code}")
            print(f"Districts in {test_state}: {r.json()}")
        else:
            print("\nSkipping Step 3: No states found in DB (Sync data first).")
    
    print("\nTest Complete.")

if __name__ == "__main__":
    test_options()
