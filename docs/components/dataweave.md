# DataWeave 2

**Files:** `src/main/resources/modules/*.dwl` and `<ee:transform>` CDATA in XML

## What it is

Mule’s transformation language. Prefer **modules on the classpath** (`import * from modules::portal`) for reusable rules; keep flow transforms thin.

## Modules in this repo

| Module | Apps | Purpose |
|---|---|---|
| `errors.dwl` | all | Canonical error JSON + HTTP mapping |
| `headers.dwl` | all | Correlation + outbound headers |
| `fulfillment.dwl` | process | Credit and status functions (MUnit covered) |
| `portal.dwl` | experience | UX labels and stock health (MUnit covered) |

## Tips

- `output application/java` for variables you will store in Object Store or reuse in connectors
- `output application/json` only at the HTTP boundary
- `p('app.name')` reads properties
- Avoid `write(payload, "application/json")` unless you must; typed objects are cheaper

MUnit in this project tests DataWeave **without** spinning HTTP, which is the fastest way to lock business rules.
