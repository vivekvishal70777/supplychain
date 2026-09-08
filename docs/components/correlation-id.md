# Correlation ID

**Files:** `apikit-router.xml` first transform; `modules/headers.dwl`

## What it is

A single UUID that follows **one business action** across Experience → Process → ERP/WMS/TMS logs.

Algorithm:

1. Read `X-Correlation-Id` or `x-correlation-id`
2. If blank, `uuid()`
3. Set `vars.correlationId` and echo it on the HTTP response
4. Copy it on every outbound `http:request`

## Why supply chain needs it

A missing allocation might be WMS 409 or TMS timeout. Support asks for the correlation id from the portal error JSON (`correlationId` field) and greps all five apps.

Put `%X{correlationId}` in log4j2 (this repo does). Optionally use the JSON logger module in EE to inject it as a field.
