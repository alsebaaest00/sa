#!/usr/bin/env python3
"""Quick API test script"""

import json

import requests

API_URL = "http://localhost:8000"


def print_response(response):
    """Print formatted response"""
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception:
        print(response.text)
    print("-" * 50)


def test_api():
    """Test all API endpoints"""
    print("🧪 Testing SA Platform API")
    print("=" * 50)

    # Test 1: Root
    print("\n1️⃣ Testing root endpoint...")
    response = requests.get(f"{API_URL}/")
    print_response(response)

    # Test 2: Health check
    print("\n2️⃣ Testing health check...")
    response = requests.get(f"{API_URL}/api/v1/health")
    print_response(response)

    # Test 3: Config status
    print("\n3️⃣ Testing config status...")
    response = requests.get(f"{API_URL}/api/v1/config/status")
    print_response(response)

    # Test 4: List outputs
    print("\n4️⃣ Testing list outputs...")
    response = requests.get(f"{API_URL}/api/v1/outputs")
    print_response(response)

    # Test 5: Audio generation (should work with gTTS fallback)
    print("\n5️⃣ Testing audio generation...")
    response = requests.post(
        f"{API_URL}/api/v1/audio/generate",
        json={
            "text": "مرحباً بكم في منصة SA",
            "voice": "Adam",
            "language": "ar",
        },
    )
    print_response(response)

    # Test 6: Prompt improvement (may fail if no OpenAI key)
    print("\n6️⃣ Testing prompt improvement...")
    response = requests.post(
        f"{API_URL}/api/v1/suggestions/improve",
        json={"prompt": "a dog in a park", "content_type": "image"},
    )
    print_response(response)

    print("\n✅ API tests completed!")


if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API at", API_URL)
        print("Make sure API is running: ./start_api.sh")
    except Exception as e:
        print(f"❌ Error: {e}")
