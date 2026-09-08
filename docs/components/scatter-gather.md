# Scatter-Gather

**Where:** Process `implementation.xml` (create order) and `health.xml` (`/ready`)

## What it is

Parallel `<route>` execution. The payload after Scatter-Gather is a map of route results (`payload[0]`, `payload[1]` in insertion order for the aggregator in Mule 4).

## Why fulfillment uses it

Customer credit (ERP) and inventory peek (WMS) are **independent reads**. Doing them in sequence wastes 100–200ms per order at volume. Timeout on the component (`timeout="10000"`) fails the whole scatter if one system hangs — better than a stuck thread.

## Watch-outs

- One route error fails the scatter unless you wrap the route in `try` / `on-error-continue`
- Do not put non-idempotent POSTs in scatter without a design for partial success
- `/ready` uses a **short** timeout so probes fail fast
