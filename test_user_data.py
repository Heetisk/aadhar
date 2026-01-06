import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_endpoints():
    # 2. Upload CSV
    print(f"Uploading testingdata.csv...")
    try:
        files = {'file': open('testingdata.csv', 'rb')}
        r = requests.post(f"{BASE_URL}/upload", files=files)
        print("Upload:", r.status_code, r.json())
        if r.status_code != 200:
            print("Upload failed, stopping test.")
            return
    except FileNotFoundError:
        print("testingdata.csv not found!")
        return

    # 3. Summary
    r = requests.get(f"{BASE_URL}/summary")
    print("Summary:", r.json())
    
    # 4. Trends State (Pick a state from the file if known, e.g., Gujarat)
    r = requests.get(f"{BASE_URL}/trends/state?state=Gujarat")
    print("Trends State (Gujarat):", r.json()[:2]) # Log first 2

    # 5. Trends District
    r = requests.get(f"{BASE_URL}/trends/district?district=Bhavnagar")
    print("Trends District (Bhavnagar):", r.json()[:2]) # Log first 2
    
    # 6. Age Comparison
    r = requests.get(f"{BASE_URL}/age-comparison")
    print("Age Comparison:", r.json())

    # 7. Anomalies
    r = requests.get(f"{BASE_URL}/anomalies")
    print("Anomalies:", r.json()[:2])

if __name__ == "__main__":
    test_endpoints()
