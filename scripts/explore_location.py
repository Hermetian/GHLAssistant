#!/usr/bin/env python3
"""Explore GHL location-level API endpoints."""

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
        "location_id": "xQhURhAeK9889aDD69Fr",
    }


def make_request(client, endpoint, session, method="GET", data=None):
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
        if method == "GET":
            resp = client.get(url, headers=headers)
        elif method == "POST":
            resp = client.post(url, headers=headers, json=data)
        return resp.status_code, resp.json() if resp.status_code == 200 else resp.text
    except Exception as e:
        return None, str(e)


def explore():
    """Explore location-level endpoints."""
    session = load_session()
    loc_id = session["location_id"]
    company_id = session["company_id"]

    print("=" * 70)
    print(f"GHL LOCATION API EXPLORATION")
    print(f"Location ID: {loc_id}")
    print("=" * 70)

    # Location-level endpoints
    endpoints = {
        # Location info
        "Location Details": f"/locations/{loc_id}",
        "Location Settings": f"/locations/{loc_id}/settings",
        "Location Custom Values": f"/locations/{loc_id}/customValues",

        # Contacts
        "Contacts Search": f"/contacts/?locationId={loc_id}&limit=10",
        "Contacts List": f"/contacts/search?locationId={loc_id}&page=1&pageLimit=10",

        # Conversations
        "Conversations": f"/conversations/?locationId={loc_id}&limit=5",
        "Conversations Search": f"/conversations/search?locationId={loc_id}",

        # Calendar
        "Calendars": f"/calendars/?locationId={loc_id}",
        "Calendar Services": f"/calendars/services?locationId={loc_id}",

        # Opportunities/Pipelines
        "Pipelines": f"/opportunities/pipelines?locationId={loc_id}",
        "Opportunities": f"/opportunities/search?locationId={loc_id}&limit=10",

        # Workflows
        "Workflows": f"/workflows/?locationId={loc_id}",

        # Campaigns
        "Campaigns": f"/campaigns/?locationId={loc_id}",

        # Forms & Surveys
        "Forms": f"/forms/?locationId={loc_id}",
        "Surveys": f"/surveys/?locationId={loc_id}",

        # Funnels
        "Funnels": f"/funnels/?locationId={loc_id}",

        # Phone
        "Phone Numbers": f"/phone-numbers/?locationId={loc_id}",
        "Inbound Calls": f"/inbound-calls?locationId={loc_id}&limit=5",

        # SMS
        "SMS Templates": f"/sms/templates?locationId={loc_id}",

        # Email
        "Email Templates": f"/emails/templates?locationId={loc_id}",

        # Tags
        "Tags": f"/tags/?locationId={loc_id}",

        # Users assigned to location
        "Location Users": f"/locations/{loc_id}/users",

        # Custom Fields
        "Custom Fields": f"/locations/{loc_id}/customFields",

        # Triggers/Automations
        "Triggers": f"/triggers?locationId={loc_id}",

        # Tasks
        "Tasks": f"/tasks?locationId={loc_id}",

        # Notes
        "Notes": f"/notes?locationId={loc_id}",
    }

    with httpx.Client(timeout=30) as client:
        for name, endpoint in endpoints.items():
            status, data = make_request(client, endpoint, session)
            print(f"\n{'='*70}")
            print(f"{name}")
            print(f"Endpoint: {endpoint[:70]}")
            print(f"Status: {status}")

            if status == 200:
                if isinstance(data, dict):
                    keys = list(data.keys())[:10]
                    print(f"Keys: {keys}")

                    # Count lists
                    for key in keys:
                        if isinstance(data[key], list):
                            print(f"  {key}: {len(data[key])} items")
                        elif isinstance(data[key], dict):
                            subkeys = list(data[key].keys())[:5]
                            print(f"  {key}: {subkeys}")

                    preview = json.dumps(data, indent=2)[:500]
                    print(f"Preview:\n{preview}")
                else:
                    print(f"Data: {str(data)[:300]}")
            elif status:
                print(f"Error: {str(data)[:150]}")


if __name__ == "__main__":
    explore()
