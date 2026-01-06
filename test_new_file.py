import requests
import json

BASE_URL = "http://127.0.0.1:8000"
FILENAME = "19eac040-0b94-49fa-b239-4f2fd8677d53_fdff22d98b88529b8dac3ef1e0f0a5d5.csv"

def test_endpoints():
    print(f"Uploading {FILENAME}...")
    try:
        files = {'file': open(FILENAME, 'rb')}
        r = requests.post(f"{BASE_URL}/upload", files=files)
        print("Upload:", r.status_code, r.json())
        if r.status_code != 200:
            print("Upload failed, stopping test.")
            return
    except FileNotFoundError:
        print(f"{FILENAME} not found!")
        return

    # 3. Summary
    r = requests.get(f"{BASE_URL}/summary")
    print("Summary:", r.json())
    
    # 4. Trends State (Gujarat seems to be in the file)
    r = requests.get(f"{BASE_URL}/trends/state?state=Gujarat")
    print("Trends State (Gujarat) - First 2:", r.json()[:2])

    # 5. Trends District (Surat is in the file)
    r = requests.get(f"{BASE_URL}/trends/district?district=Surat")
    print("Trends District (Surat) - First 2:", r.json()[:2])
    
if __name__ == "__main__":
    test_endpoints()
