# Until-Successful (retry)

**Where:** Process `impl-orchestrate-fulfillment` around HTTP Request

## What it is

Retries the inner processors until they succeed or `maxRetries` is exhausted. `millisBetweenRetries` should be small (400–750ms) for user-facing HTTP.

## When to use it

| Call | Retry? |
|---|---|
| GET customer | Yes (safe) |
| POST PO with idempotency key | Yes |
| POST allocate without idempotency | Risky — WMS might double-allocate. Prefer WMS-side idempotency |
| PATCH cancel | Usually yes |

Retries do **not** replace a circuit breaker. If ERP is down, retries amplify load — pair with `impl-check-circuit`.
