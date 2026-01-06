import requests
import os

BASE_URL = "http://127.0.0.1:8000"
FILE_PATH = "19eac040-0b94-49fa-b239-4f2fd8677d53_fdff22d98b88529b8dac3ef1e0f0a5d5.csv"

def test_specific_csv():
    print(f"Testing upload for: {FILE_PATH}")
    
    if not os.path.exists(FILE_PATH):
        print("Error: File not found!")
        return

    # 1. Clear Data (optional, but good for clean test)
    print("\n1. Clearing Database...")
    try:
        requests.delete(f"{BASE_URL}/clear-data")
    except Exception as e:
        print(f"Warning: Could not clear data (maybe endpoint missing?): {e}")

    # 2. Upload File
    print("\n2. Uploading CSV...")
    try:
        with open(FILE_PATH, "rb") as f:
            files = {"file": (FILE_PATH, f, "text/csv")}
            r = requests.post(f"{BASE_URL}/upload", files=files)
            print(f"Status: {r.status_code}")
            print(f"Response: {r.json()}")
            r.raise_for_status()
    except Exception as e:
        print(f"Upload Failed: {e}")
        return

    # 3. Verify Summary
    print("\n3. Verifying Summary...")
    try:
        r = requests.get(f"{BASE_URL}/summary")
        print(f"Summary: {r.json()}")
    except Exception as e:
        print(f"Summary Check Failed: {e}")

if __name__ == "__main__":
    test_specific_csv()
