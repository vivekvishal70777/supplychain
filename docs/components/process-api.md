# Process API — Fulfillment (`sc-prc-fulfillment-api`)

**File:** `sc-prc-fulfillment-api/src/main/mule/implementation.xml`  
**Port (local):** 8082

## What it is

The Process API **owns the business process** "place and fulfill an order". It is the saga coordinator: credit, PO create, allocate, book, compensate.

## Orchestration sequence

1. Validate `X-Idempotency-Key` and replay if seen.
2. **Scatter-Gather:** ERP customer GET ∥ WMS inventory GET (first SKU snapshot).
3. Credit rules (blocked / payables ≥ limit) → `APP:CREDIT_HOLD`.
4. `until-successful` POST ERP purchase order.
5. POST WMS allocate; on failure **cancel PO**.
6. POST TMS shipment; on failure **release allocation**.
7. Persist fulfillment record; return 201.

## Patterns to study in this app

- Scatter-Gather (`health.xml` and create-order)
- Until-Successful around HTTP Request
- Circuit breaker sub-flows (`impl-check-circuit`)
- Compensation sub-flows
- Scheduler heartbeat every 15 minutes
- HTTP Request configs per system (`global.xml`)

## Production notes

Timeouts on `/ready` are short (4s) so Kubernetes can fail a replica quickly. Create-order timeouts are longer (system YAML `responseTimeout`). Do not mix those values.
