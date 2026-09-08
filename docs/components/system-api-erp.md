# System API — ERP (`sc-sys-erp-api`)

**Port (local):** 8091  
**Seed data:** `src/main/resources/data/customers.json`, `products.json`

## What it is

A **System API** wraps one system of record. Here that system is a simulated ERP: customers, product master, purchase orders.

In production this XML stays, but `impl-create-po` would become:

- SAP S/4HANA OData / BAPI via HTTP Request or SAP connector
- Oracle EBS PL/SQL via Database connector
- DataWeave maps IDoc/OData → canonical `PurchaseOrder`

## Resources

| Method | Path | Behavior |
|---|---|---|
| GET | `/customers/{id}` | 404 `APP:NOT_FOUND` |
| GET | `/products/{sku}` | Product master including `hazardous` |
| POST | `/purchase-orders` | Idempotent create; blocked customer → `APP:CREDIT_HOLD` |
| PATCH | `/purchase-orders/{id}` | Confirm / cancel; shipped POs conflict |

## Learning focus

Lazy seed (`impl-ensure-seed`) shows a safe way to load classpath JSON into Object Store on first use without a Scheduler hammer.

Replace Object Store with JDBC and you still keep the same RAML — that is the point of a System API.
