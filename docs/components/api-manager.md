# API Autodiscovery, API Manager, policies

**Example:** `sc-exp-portal-api/src/main/resources/examples/api-autodiscovery.xml.example`

## What it is

Autodiscovery links a running Mule app to an **API Manager** instance (`apiId`). Policies then execute in the API gateway / embedded policy chain **before** your listener logic.

## Policies to apply on Experience (typical)

| Policy | Why |
|---|---|
| Client ID Enforcement | App identity for partners |
| Rate Limiting / Spike Control | Protect WMS from traffic storms |
| JWT Validation | Portal SSO |
| CORS | Browser portal |
| Header injection | Force correlation if missing (optional) |

System APIs: **no public policies**; restrict at the network. If you must expose them, use a separate API Manager instance on an internal DLB.

Do not implement rate limiting with Object Store in the app if API Manager is available — operations need a single place to change SLA tiers.
