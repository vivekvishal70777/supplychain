# Validation

## Layers in this platform

1. **RAML / APIKit** — types, required headers (`X-Idempotency-Key` on create), enums (`STANDARD|EXPEDITED|OVERNIGHT`).
2. **Choice + raise-error** — semantic rules APIKit cannot express (blocked customer, empty lines, illegal PO status).
3. **mule-validation-module** — on the classpath for JSON Schema / `is-not-empty` if you add `<validation:is-not-null>` later.

The Validation module is a dependency even when unused in XML so you can drop in `<validation:matches-regex>` without a POM change.

## What to validate where

| Concern | Layer |
|---|---|
| JSON types, dates, enums | RAML |
| Credit vs limit | Process (needs ERP data) |
| SKU exists | ERP System API |
| Qty ≤ available | WMS System API |

Do not duplicate credit logic in Experience.
