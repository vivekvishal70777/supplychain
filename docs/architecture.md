# Architecture

## Business domain

GlobalMart sells industrial goods through a partner portal. A **fulfillment** is the process of turning a customer order into:

1. An ERP **purchase order** (commercial record, credit).
2. A WMS **allocation** (physical stock reserved).
3. A TMS **shipment** (carrier booking + tracking).

That split matches how real supply-chain landscapes are owned: finance owns ERP, operations owns WMS, logistics owns TMS. MuleSoft sits in the middle so each system keeps its own model while the process layer owns the **saga**.

## API-led connectivity

| Layer | Who calls it | Stability | This repo |
|---|---|---|---|
| Experience | Mobile, portal, B2B EDI gateway | Changes with UX | `sc-exp-portal-api` |
| Process | Other Mule apps / Experience APIs | Changes with business process | `sc-prc-fulfillment-api` |
| System | Process APIs only | Changes with the system of record | `sc-sys-*-api` |

**Rule:** Experience never calls System. Process never exposes UX-specific field names. System never contains orchestration.

Why it matters in supply chain: a new storefront can be an extra Experience API without touching SAP mappings. A warehouse swap (Manhattan → SAP EWM) is a System API rewrite; Process stays on `POST /inventory/allocate`.

## Canonical model vs system model

Process APIs speak a **canonical** JSON model (`fulfillmentId`, `allocationId`, money as `{amount, currency}`). System APIs may later map IDoc / OData / SOAP into that shape with DataWeave. The local Object Store implementations already emit canonical JSON so you can study the flows without vendor XML.

## Runtime topology

```
                ┌──────────── API Manager (policies) ────────────┐
Client ─HTTPS──►│ Rate limit, Client ID, JWT, SLA                │
                └────────────────────┬───────────────────────────┘
                                     ▼
                           Experience replica x2
                                     ▼
                           Process replica x2
                          /        |         \
                       ERP       WMS        TMS
```

On CloudHub 2.0 / Runtime Fabric:

- Replicas ≥ 2, rolling deploy, spread across nodes (parent POM).
- Object Store v2 for CloudHub so idempotency survives redeploy.
- Anypoint MQ replaces in-app VM queues for tracking events when you need cluster-wide pub/sub.

## Transaction style (saga)

There is no distributed XA across SAP + WMS + TMS. The process API uses **orchestration + compensation**:

| Step | Success | Compensation on later failure |
|---|---|---|
| Credit + inventory scatter-gather | Continue | None (read-only) |
| Create ERP PO | Store `poId` | `PATCH` PO to `CANCELLED` |
| WMS allocate | Store `allocationId` | `POST /inventory/release` |
| TMS book | Return tracking | Release allocation; leave PO cancelled or flagged |

## Security layers

1. **Edge:** mTLS or HTTPS at the load balancer.
2. **API Manager:** Client ID Enforcement, JWT validation, rate limiting, IP allowlist — applied by autodiscovery, not by embedding secrets in flows.
3. **App:** correlation ID, no stack traces in 500 bodies, `secureProperties` in `mule-artifact.json`.
4. **Secrets:** Secure Configuration Properties + secrets manager. See the example XML under `sc-exp-portal-api/src/main/resources/examples/`.

## Observability

- `X-Correlation-Id` is generated if missing and copied on every outbound HTTP call.
- `log4j2.xml` logs the correlation MDC key.
- `/health` = process liveness (load balancer).
- `/ready` = dependencies reachable (orchestration layer scatter-gathers system health).

## Why Object Store instead of a database here

System APIs in **production** would use SAP S/4HANA, JDBC, or vendor connectors. Object Store keeps this repo self-contained and demonstrates the same connector you will use for idempotency and circuit state in production.
