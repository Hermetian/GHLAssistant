#!/usr/bin/env python3
"""Test direct API calls using captured token."""

import json
import httpx
from pathlib import Path


def load_token():
    """Load token from latest session."""
    log_dir = Path(__file__).parent.parent / "data" / "network_logs"
    sessions = sorted(log_dir.glob("session_*.json"))
    if not sessions:
        raise FileNotFoundError("No sessions found")

    with open(sessions[-1]) as f:
        data = json.load(f)

    return data.get("auth", {}).get("access_token")


def test_api():
    """Test API calls."""
    token = load_token()
    if not token:
        print("No token found!")
        return

    print(f"Token: {token[:50]}...")
    print()

    # Headers from captured requests - MUST include version, channel, source
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Origin": "https://app.gohighlevel.com",
        "Referer": "https://app.gohighlevel.com/",
        "version": "2021-07-28",  # Required!
        "channel": "APP",  # Required!
        "source": "WEB_USER",  # Required!
    }

    base_url = "https://backend.leadconnectorhq.com"

    # IDs from our session
    user_id = "dJv1aXj2NN2nV8r6xcF6"
    company_id = "AJqfXhpsvU0HR0Wcd6YH"

    # Endpoints to test
    endpoints = [
        f"/users/{user_id}",
        f"/oauth/keys/?accountId={company_id}&type=Company&limit=5&skip=0",
        f"/companies/{company_id}/labs/featureFlags",
        f"/notifications/users/{user_id}?limit=5&skip=0&deleted=false",
    ]

    with httpx.Client(timeout=30) as client:
        for endpoint in endpoints:
            url = f"{base_url}{endpoint}"
            print(f"Testing: {endpoint[:60]}...")

            try:
                resp = client.get(url, headers=headers)
                print(f"  Status: {resp.status_code}")

                if resp.status_code == 200:
                    data = resp.json()
                    # Pretty print first 500 chars
                    preview = json.dumps(data, indent=2)[:500]
                    print(f"  Response preview:\n{preview}")
                else:
                    print(f"  Error: {resp.text[:200]}")

            except Exception as e:
                print(f"  Error: {e}")

            print()


if __name__ == "__main__":
    test_api()
