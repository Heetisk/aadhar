import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_clear_data():
    print("1. Seed data via Sync...")
    r = requests.post(f"{BASE_URL}/sync-api?limit=10")
    print(f"Sync: {r.status_code}")
    
    # Check count
    r = requests.get(f"{BASE_URL}/summary")
    count = r.json().get('total_enrolments')
    print(f"Count before clear: {count}")
    
    if count == 0:
        print("Error: No data synced, cannot test clear.")
        return

    print("\n2. Clear Data...")
    r = requests.delete(f"{BASE_URL}/clear-data")
    print(f"Clear Response: {r.status_code} - {r.json()}")
    
    # Check count again
    r = requests.get(f"{BASE_URL}/summary")
    new_count = r.json().get('total_enrolments')
    print(f"Count after clear: {new_count}")
    
    if new_count == 0:
        print("\nSUCCESS: Database successfully cleared.")
    else:
        print("\nFAILURE: Data still exists.")

if __name__ == "__main__":
    test_clear_data()
