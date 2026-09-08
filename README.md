# GlobalMart Supply Chain Integration Platform

Production-style **MuleSoft 4** (Java 17) solution for order-to-fulfillment. It follows **API-led connectivity**: Experience, Process, and System APIs. Downstream ERP / WMS / TMS systems are simulated with Object Store so you can run and learn locally without SAP or a warehouse product.

## What you get

| Application | Layer | Local port | Responsibility |
|---|---|---|---|
| `sc-exp-portal-api` | Experience | 8081 | Partner portal REST shape, paging, ASN intake |
| `sc-prc-fulfillment-api` | Process | 8082 | Orchestration, retries, compensation, circuit breaker |
| `sc-sys-erp-api` | System | 8091 | Customers, products, purchase orders |
| `sc-sys-wms-api` | System | 8092 | Inventory, allocation, warehouses |
| `sc-sys-tms-api` | System | 8093 | Carriers, shipment booking, async tracking |

Happy path: **portal order → credit check + inventory snapshot (scatter-gather) → ERP PO → WMS allocate → TMS book → tracking number**. Failures compensate (cancel PO / release allocation). Duplicate posts are absorbed with `X-Idempotency-Key`.

```
Portal / ops UI
      │  HTTPS + policies (API Manager)
      ▼
sc-exp-portal-api
      │
      ▼
sc-prc-fulfillment-api
      │  scatter-gather + until-successful
      ├──► sc-sys-erp-api  (customer, PO)
      ├──► sc-sys-wms-api  (allocate / release)
      └──► sc-sys-tms-api  (book + VM tracking events)
```

## Learning path

Start here, in order:

1. [Architecture](docs/architecture.md)
2. [Learning index — every component](docs/components/README.md)
3. [Run locally](docs/local-run.md)
4. [Deploy and operate](docs/deployment.md)

Each Mule XML file, connector, and pattern has a dedicated page under `docs/components/`.

## Prerequisites

- JDK 17
- Maven 3.9+
- Anypoint Studio 7.16+ **or** Mule Runtime 4.6.x Enterprise (MUnit and `mule-application` packaging need EE)
- Optional: Anypoint Platform org for API Manager policies and CloudHub 2.0

This repository still validates XML / RAML / YAML / JSON in GitHub Actions **without** a Mule license (`scripts/validate-artifacts.py`).

## Quick start (Studio)

1. Import the Maven parent `pom.xml`.
2. Set VM argument `-M-Dmule.env=local` (already defaulted via `application.properties`).
3. Run the three System APIs, then Process, then Experience.
4. Import `postman/Supply-Chain-Platform.postman_collection.json`.
5. `POST http://localhost:8081/api/orders` with header `X-Idempotency-Key: demo-order-001`.

Seed customers: `CUST-1001` (healthy), `CUST-1002` (near credit limit), `CUST-2099` (blocked). Seed SKU: `SKU-WIDGET-A`.

## Production practices included

- API-led layers with RAML 1.0 + APIKit
- Canonical JSON error contract and correlation IDs
- Environment-specific YAML (`local` / `dev` / `prod`)
- Global error handler and custom `APP:*` error types
- Object Store persistence, idempotency, circuit-breaker state
- HTTP Request timeouts, `until-successful` retries
- Scatter-Gather, For-Each, Choice, Async, Scheduler
- VM queues + dead-letter queue for tracking events
- Compensation (saga-style) on partial failure
- Health and readiness probes
- Structured logging placeholders (`log4j2.xml`)
- MUnit tests for DataWeave domain logic
- CloudHub 2.0 deployment skeleton in the parent POM
- API Autodiscovery and Secure Properties **examples** (not started locally so the apps boot without secrets)

## License / sample data

Sample customers and SKUs are fictitious. Replace System API persistence with real SAP / Manhattan / Oracle Transportation adapters in production.
