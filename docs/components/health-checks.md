# Health and readiness

**Files:** `health.xml` in every app

## Liveness (`GET /health`)

"This JVM answers HTTP." No downstream calls. Load balancers use this so a hung app is removed.

## Readiness (`GET /ready`)

- System APIs: seed Object Store then `READY`
- Process: Scatter-Gather to all three system `/health` endpoints
- Experience: Process `/health`

If Process `/ready` is green, an order has a chance. If only Experience is up, the portal would 503 on submit — fail the replica instead.

## Kubernetes mapping

- `livenessProbe` → `/api/health`
- `readinessProbe` → `/api/ready` (Process / Experience)
