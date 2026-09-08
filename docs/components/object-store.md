# Object Store connector

**Files:** `global.xml` object-store definitions; `os:store` / `os:retrieve` / `os:contains`

## What it is

Key-value storage inside the Mule runtime (or Object Store v2 on CloudHub). Used here for:

1. Simulated systems of record (customers, inventory, shipments)
2. Idempotency keys
3. Circuit breaker state
4. Experience order index and ASNs

## Config knobs

- `persistent` — false on local so Studio restarts clean; true in prod
- `entryTtl` + unit — idempotency keys expire (24h here)
- `maxEntries` — guard memory

## Errors

`OS:KEY_NOT_FOUND` is normal. Catch it with `on-error-continue` when a missing key means "empty list", and `on-error-propagate` mapped to `APP:NOT_FOUND` when a missing key is a 404.
