# Idempotency

**Where:** ERP `POST /purchase-orders`, Process `POST /fulfillment/orders`, Experience forwards the header

## What it is

Clients retry (mobile timeouts, API gateways). Without idempotency you book **two trucks**.

Header: `X-Idempotency-Key` (required on create). Stored in `idempotency-store` mapping key → original resource. Replay returns the stored body (HTTP 200 on replay in ERP; Process same).

## Rules

- Key is caller-defined (UUID). Never derive only from customerId (two legitimate orders would collapse).
- TTL 24h matches typical "user retries the submit button"
- POST without the header → `APP:VALIDATION`
- Must be applied **before** side effects (check `os:contains` first)

Process passes the **same** key to ERP so a retried saga does not create a second PO if Process crashed after ERP success.
