# Compensation (saga)

**Where:** `impl-compensate-cancel-po`, `impl-compensate-release-allocation`

## What it is

Because there is no XA transaction across ERP + WMS + TMS, Process undoes **completed steps** when a later step fails.

```
PO created ──► allocate fails ──► PATCH PO CANCELLED
allocated  ──► TMS fails     ──► POST inventory/release
cancel API ─────────────────────► release allocation
```

Compensation itself is wrapped in `on-error-continue` so a compensation outage is logged for ops (manual repair) while the customer still receives the original business error.

## Production hardening

- Outbox table of "compensation pending"
- Scheduler replays failed compensations
- WMS release and ERP cancel must be idempotent
