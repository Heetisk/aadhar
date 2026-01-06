import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_endpoints():
    # 1. Check Root
    try:
        r = requests.get(f"{BASE_URL}/")
        print("Root Check:", r.json())
    except Exception as e:
        print("Server not running?", e)
        return

    # 2. Upload CSV
    files = {'file': open('test_data.csv', 'rb')}
    r = requests.post(f"{BASE_URL}/upload", files=files)
    print("Upload:", r.status_code, r.json())

    # 3. Summary
    r = requests.get(f"{BASE_URL}/summary")
    print("Summary:", r.json())
    
    # 4. Trends State
    r = requests.get(f"{BASE_URL}/trends/state")
    print("Trends State:", r.json())

    # 5. Trends District
    r = requests.get(f"{BASE_URL}/trends/district")
    print("Trends District:", r.json())
    
    # 6. Age Comparison
    r = requests.get(f"{BASE_URL}/age-comparison")
    print("Age Comparison:", r.json())

    # 7. Anomalies
    r = requests.get(f"{BASE_URL}/anomalies")
    print("Anomalies:", r.json())

if __name__ == "__main__":
    test_endpoints()
