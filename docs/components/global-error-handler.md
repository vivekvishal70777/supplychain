# Global error handler

**Files:** `src/main/mule/global-error-handler.xml` in every app  
**Wiring:** `<configuration defaultErrorHandler-ref="global-error-handler"/>`

## What it is

A named `<error-handler>` that maps Mule error types to HTTP status + canonical JSON (`modules/errors.dwl`).

Order of `on-error-propagate` matters: more specific types (`APP:NOT_FOUND`) before `ANY`.

## Error types used in this platform

| Type | Typical HTTP | Meaning |
|---|---|---|
| `APP:NOT_FOUND` | 404 | Business entity missing |
| `APP:VALIDATION` | 422 | Semantic validation (beyond RAML) |
| `APP:CREDIT_HOLD` | 422 | ERP credit / blocked customer |
| `APP:BACKORDER` | 409 | Cannot allocate |
| `APP:CONFLICT` | 409 | Illegal status transition |
| `APP:CIRCUIT_OPEN` | 503 | Downstream isolated |
| `APIKIT:*` | 400/404/405 | Contract violation |
| `HTTP:CONNECTIVITY` / `TIMEOUT` | 503/504 | Network |
| `ANY` | 500 | Unknown — **no** `error.description` internals in prod body |

Process API maps connectivity to a **generic** "downstream unavailable" message so portal users never see "Connection refused to wms:8092".
