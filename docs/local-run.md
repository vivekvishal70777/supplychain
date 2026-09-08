# Run locally

## Order of startup

System APIs have no upstream dependencies. Process calls all three. Experience calls Process.

1. `sc-sys-erp-api` — port **8091**
2. `sc-sys-wms-api` — port **8092**
3. `sc-sys-tms-api` — port **8093**
4. `sc-prc-fulfillment-api` — port **8082**
5. `sc-exp-portal-api` — port **8081**

In Anypoint Studio: Run As → Mule Application on each module. Ensure `mule.env=local` (default in `application.properties`).

From Maven (EE runtime on the machine):

```bash
cd sc-sys-erp-api && mvn mule:run -Dmule.env=local
```

## Smoke tests

```bash
curl -s http://localhost:8091/api/health
curl -s http://localhost:8092/api/health
curl -s http://localhost:8093/api/health
curl -s http://localhost:8082/api/health
curl -s http://localhost:8081/api/health
```

Place an order:

```bash
curl -s -X POST http://localhost:8081/api/orders \
  -H 'Content-Type: application/json' \
  -H 'X-Idempotency-Key: demo-order-001' \
  -H 'X-Correlation-Id: learn-001' \
  -d '{
    "customerId": "CUST-1001",
    "requestedShipDate": "2026-09-20",
    "serviceLevel": "STANDARD",
    "lines": [{"sku": "SKU-WIDGET-A", "quantity": 4}],
    "shipTo": {"line1": "500 Market St", "city": "Chicago", "postalCode": "60601", "country": "US"}
  }'
```

Replay the same idempotency key — you should get the original fulfillment, not a second shipment.

Blocked customer (`CUST-2099`) should return **422** `APP:CREDIT_HOLD`.

APIKit consoles (local / dev only): `http://localhost:8081/console/`.

## Artifact validation without Mule

```bash
python3 scripts/validate-artifacts.py
```

## Common issues

| Symptom | Cause |
|---|---|
| Process `/ready` is 500 | A System API is down or port mismatch in `config-local.yaml` |
| 404 on `/api/orders` | Listener path is `/api/*`; do not omit `/api` |
| Studio won't package | Parent POM `packaging=pom`; import **modules**, not only the root |
| Secure properties fail | Those configs are examples only; do not copy them in until you have a key |
