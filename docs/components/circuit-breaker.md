# Circuit breaker

**Where:** Process `impl-check-circuit` / `impl-record-circuit-failure` + `circuit-store`

## What it is

If ERP has failed `circuit.failureThreshold` times, further calls fail fast with `APP:CIRCUIT_OPEN` until `openUntil` (now + `circuit.openMs`).

This is a **teaching implementation** using Object Store. Production options:

- Anypoint Circuit Breaker module
- Resilience4j via Java / custom module
- API Manager spike control (edge, not per-dependency)

## Why

`until-successful` against a dead SAP burns thread pools and makes WMS look slow too. The circuit isolates ERP so WMS traffic continues for other processes (inventory inquiry).

Call `impl-record-circuit-failure` from an `on-error` around ERP HTTP (wire-up left partial so you can practice connecting it — check-circuit is on the ERP scatter route).
