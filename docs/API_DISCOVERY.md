# GHL API Discovery

Reverse-engineered from browser traffic capture on 2025-12-23.

## Authentication

**Base URL:** `https://backend.leadconnectorhq.com`

**Required Headers:**
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
Accept: application/json, text/plain, */*
version: 2021-07-28
channel: APP
source: WEB_USER
```

Token can be obtained via browser session capture or OAuth flow.

## Account Hierarchy

```
Company (Agency)
└── Location (Sub-account)
    ├── Contacts
    ├── Workflows
    ├── Calendars
    ├── Pipelines/Opportunities
    └── etc.
```

## IDs Discovered

| Type | ID | Name |
|------|-----|------|
| Company | `AJqfXhpsvU0HR0Wcd6YH` | Discorp |
| Location | `xQhURhAeK9889aDD69Fr` | Discorp |
| User | `dJv1aXj2NN2nV8r6xcF6` | Robert Cordwell |

---

## Company-Level Endpoints (200 OK)

### User Profile
```
GET /users/{userId}
```
Returns user info, permissions, 452+ scopes.

### Company Info
```
GET /companies/{companyId}
```
Returns company name, address, plan, settings.

### Locations Search
```
GET /locations/search?companyId={companyId}
```
Returns list of locations (sub-accounts).

### Billing
```
GET /internal-tools/billing/company/{companyId}/plan
GET /internal-tools/billing/company-info/{companyId}
```
Returns plan details, Stripe info, trial status.

### Feature Flags
```
GET /companies/{companyId}/labs/featureFlags
```
Returns enabled features and experiments.

### OAuth/API Keys
```
GET /oauth/keys/?accountId={companyId}&type=Company&limit=10
```
Returns API keys for the company.

---

## Location-Level Endpoints (200 OK)

### Location Details
```
GET /locations/{locationId}
```
Returns location info, timezone, business details.

### Custom Values
```
GET /locations/{locationId}/customValues
```
Returns custom value fields (merge fields).

### Custom Fields
```
GET /locations/{locationId}/customFields
```
Returns custom contact fields.

### Contacts
```
GET /contacts/?locationId={locationId}&limit=10
```
Returns contacts with pagination meta.

### Conversations
```
GET /conversations/search?locationId={locationId}
```
Returns conversations list.

### Calendars
```
GET /calendars/?locationId={locationId}
GET /calendars/services?locationId={locationId}
```
Returns calendars and booking services.

### Pipelines & Opportunities
```
GET /opportunities/pipelines?locationId={locationId}
```
Returns sales pipelines with stages.

### Workflows
```
GET /workflows/?locationId={locationId}
```
Returns automation workflows.

### Forms
```
GET /forms/?locationId={locationId}
```
Returns form builders.

### Campaigns, Surveys, Funnels
```
GET /campaigns/?locationId={locationId}
GET /surveys/?locationId={locationId}
GET /funnels/?locationId={locationId}
```

---

## Endpoints Returning 404 (Not Found or Wrong Path)

These may require different paths or parameters:
- `/phone-numbers/`
- `/sms/templates`
- `/emails/templates`
- `/tags/`
- `/triggers`
- `/tasks`
- `/notes`
- `/inbound-calls`

---

## Data Discovered

### Workflows (6)
1. New Lead Nurture (Fast 5) - Claim Offer
2. Appointment Confirmation + Reminders
3. + 4 more

### Calendars (5)
Multiple calendar types configured.

### Pipelines (2)
- Stages: New Lead → Hot Lead → etc.

### Forms (1)
- Marketing Form - Claim Offer

### Contacts (1)
- joe tempy (djt@gmail.com)

---

## Next Steps

1. Build typed API client with these endpoints
2. Capture more traffic to find CRUD operations (POST/PUT/DELETE)
3. Map workflow/trigger APIs for automation
4. Find 10DLC-related endpoints
