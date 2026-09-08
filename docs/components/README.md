# Component learning index

Every production building block in this repo is documented below. Read **what it is**, **where it lives**, and **why supply chain integrations use it**.

## Applications (API-led)

| Component | Doc |
|---|---|
| Experience API — Partner Portal | [experience-api.md](experience-api.md) |
| Process API — Fulfillment | [process-api.md](process-api.md) |
| System API — ERP | [system-api-erp.md](system-api-erp.md) |
| System API — WMS | [system-api-wms.md](system-api-wms.md) |
| System API — TMS | [system-api-tms.md](system-api-tms.md) |

## Project and packaging

| Component | Doc |
|---|---|
| Maven multi-module + Mule Maven Plugin | [mule-maven-plugin.md](mule-maven-plugin.md) |
| `mule-artifact.json` | [mule-artifact.md](mule-artifact.md) |
| Properties and `mule.env` | [properties.md](properties.md) |
| RAML + APIKit | [apikit-raml.md](apikit-raml.md) |
| log4j2 | [log4j2.md](log4j2.md) |
| MUnit | [munit.md](munit.md) |
| CI/CD | [cicd.md](cicd.md) |

## Mule runtime components

| Component | Doc |
|---|---|
| HTTP Listener | [http-listener.md](http-listener.md) |
| HTTP Request | [http-request.md](http-request.md) |
| Global error handler | [global-error-handler.md](global-error-handler.md) |
| DataWeave 2 | [dataweave.md](dataweave.md) |
| Object Store | [object-store.md](object-store.md) |
| Choice router | [choice-router.md](choice-router.md) |
| Scatter-Gather | [scatter-gather.md](scatter-gather.md) |
| Until-Successful (retry) | [until-successful.md](until-successful.md) |
| For-Each | [foreach.md](foreach.md) |
| Flow-ref and sub-flows | [flow-ref.md](flow-ref.md) |
| Async scope | [async.md](async.md) |
| Scheduler | [scheduler.md](scheduler.md) |
| VM connector + DLQ | [vm-queues.md](vm-queues.md) |
| Try / on-error-continue | [try-scope.md](try-scope.md) |
| Raise-error | [raise-error.md](raise-error.md) |
| Validation | [validation.md](validation.md) |
| Health and readiness | [health-checks.md](health-checks.md) |
| Correlation ID | [correlation-id.md](correlation-id.md) |
| Idempotency | [idempotency.md](idempotency.md) |
| Circuit breaker | [circuit-breaker.md](circuit-breaker.md) |
| Compensation / saga | [compensation.md](compensation.md) |
| API Autodiscovery and policies | [api-manager.md](api-manager.md) |
| Secure properties | [secure-properties.md](secure-properties.md) |
