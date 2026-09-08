# HTTP Request

**Files:** Process `global.xml` (`erp-httpreq`, `wms-httpreq`, `tms-httpreq`); Experience `prc-httpreq`

## What it is

Outbound HTTP. Each downstream system gets its **own** `request-config` so timeouts, TLS, and hosts do not leak across ERP vs WMS.

## Production settings to copy

- `responseTimeout` from YAML (5–8s typical for System APIs)
- URI params as a map, not string concatenation
- Always send `X-Correlation-Id` (see `modules/headers.dwl` `sysHeaders`)
- Wrap with `until-successful` only for **idempotent** or **safe-to-retry** calls (GET, or POST with idempotency key)

## TLS

Local is plain HTTP. In prod attach `tls:context` (trust store) on `http:request-connection`. Do not disable certificate validation.
