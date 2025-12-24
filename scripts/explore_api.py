#!/usr/bin/env python3
"""Explore GHL API endpoints."""

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


def make_request(client, endpoint, session):
    """Make authenticated request to GHL API."""
    headers = {
        "Authorization": f"Bearer {session['token']}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "version": "2021-07-28",
        "channel": "APP",
        "source": "WEB_USER",
    }

    url = f"https://backend.leadconnectorhq.com{endpoint}"

    try:
        resp = client.get(url, headers=headers)
        return resp.status_code, resp.json() if resp.status_code == 200 else resp.text
    except Exception as e:
        return None, str(e)


def explore():
    """Explore various endpoints."""
    session = load_session()
    user_id = session["user_id"]
    company_id = session["company_id"]

    print("=" * 70)
    print("GHL API EXPLORATION")
    print("=" * 70)

    # Endpoints to explore
    endpoints = {
        # User & Company
        "User Profile": f"/users/{user_id}",
        "Company Info": f"/companies/{company_id}",
        "Company Settings": f"/companies/{company_id}/settings",

        # Locations (sub-accounts)
        "Locations List": f"/locations?companyId={company_id}&skip=0&limit=50",

        # Contacts
        "Contacts": f"/contacts?companyId={company_id}&limit=10",

        # Workflows
        "Workflows": f"/workflows?companyId={company_id}",

        # Calendars
        "Calendars": f"/calendars?companyId={company_id}",

        # Pipelines/Opportunities
        "Pipelines": f"/pipelines?companyId={company_id}",

        # Conversations
        "Conversations": f"/conversations?companyId={company_id}&limit=5",

        # Phone/SMS
        "Phone Numbers": f"/phone-numbers?companyId={company_id}",
        "SMS Templates": f"/sms-templates?companyId={company_id}",

        # Automations
        "Triggers": f"/triggers?companyId={company_id}",
        "Campaigns": f"/campaigns?companyId={company_id}",

        # OAuth/API
        "OAuth Apps": f"/oauth/apps?companyId={company_id}",
        "OAuth Keys": f"/oauth/keys/?accountId={company_id}&type=Company&limit=10&skip=0",

        # Billing
        "Billing Plan": f"/internal-tools/billing/company/{company_id}/plan",
        "Billing Info": f"/internal-tools/billing/company-info/{company_id}",

        # Features
        "Feature Flags": f"/companies/{company_id}/labs/featureFlags",
    }

    with httpx.Client(timeout=30) as client:
        for name, endpoint in endpoints.items():
            status, data = make_request(client, endpoint, session)
            print(f"\n{'='*70}")
            print(f"{name}: {endpoint[:60]}")
            print(f"Status: {status}")

            if status == 200:
                if isinstance(data, dict):
                    # Show structure
                    keys = list(data.keys())[:10]
                    print(f"Keys: {keys}")

                    # Show counts for lists
                    for key in keys:
                        if isinstance(data[key], list):
                            print(f"  {key}: {len(data[key])} items")

                    # Pretty print first 400 chars
                    preview = json.dumps(data, indent=2)[:600]
                    print(f"Preview:\n{preview}")
                else:
                    print(f"Data: {str(data)[:400]}")
            else:
                print(f"Error: {str(data)[:200]}")


if __name__ == "__main__":
    explore()
