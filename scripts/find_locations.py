#!/usr/bin/env python3
"""Find GHL locations (sub-accounts)."""

import json
import httpx
from pathlib import Path


def load_session():
    """Load token and IDs from latest session."""
    log_dir = Path(__file__).parent.parent / "data" / "network_logs"
    sessions = sorted(log_dir.glob("session_*.json"))
    if not sessions:
        raise FileNotFoundError("No sessions found")

    with open(sessions[-1]) as f:
        data = json.load(f)

    return {
        "token": data.get("auth", {}).get("access_token"),
        "user_id": "dJv1aXj2NN2nV8r6xcF6",
        "company_id": "AJqfXhpsvU0HR0Wcd6YH",
    }


def find_locations():
    """Try various endpoints to find locations."""
    session = load_session()
    company_id = session["company_id"]
    user_id = session["user_id"]

    headers = {
        "Authorization": f"Bearer {session['token']}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "version": "2021-07-28",
        "channel": "APP",
        "source": "WEB_USER",
    }

    # Various potential endpoints for locations
    endpoints = [
        f"/saas-api/locations/search?companyId={company_id}",
        f"/saas/locations?companyId={company_id}",
        f"/agency/locations?companyId={company_id}",
        f"/locations/search?companyId={company_id}",
        f"/companies/{company_id}/locations",
        f"/users/{user_id}/locations",
        f"/agency/accounts?companyId={company_id}",
        f"/sub-accounts?companyId={company_id}",
        f"/saas-api/locations?companyId={company_id}&limit=50",
    ]

    with httpx.Client(timeout=30) as client:
        for endpoint in endpoints:
            url = f"https://backend.leadconnectorhq.com{endpoint}"
            try:
                resp = client.get(url, headers=headers)
                print(f"\n{endpoint}")
                print(f"  Status: {resp.status_code}")
                if resp.status_code == 200:
                    data = resp.json()
                    print(f"  Response: {json.dumps(data, indent=2)[:500]}")
                else:
                    text = resp.text[:200] if resp.text else "(empty)"
                    print(f"  Error: {text}")
            except Exception as e:
                print(f"  Exception: {e}")


if __name__ == "__main__":
    find_locations()
