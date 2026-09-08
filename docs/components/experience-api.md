# Experience API — Partner Portal (`sc-exp-portal-api`)

**File:** `sc-exp-portal-api/`  
**RAML:** `src/main/resources/api/sc-exp-portal-api.raml`  
**Port (local):** 8081

## What it is

The Experience API is the **only** internet-facing contract for the partner portal. It reshapes Process API payloads into UI language (`statusLabel`, `stockHealth`, paging). It does not allocate inventory or talk to SAP.

## Why it exists

Portal teams change labels weekly. Warehouse APIs must not. By isolating UX mapping in DataWeave module `modules/portal.dwl`, you can add a second Experience API later (mobile, EDI 850) without cloning fulfillment logic.

## Key flows

| RAML resource | Implementation flow | Notes |
|---|---|---|
| `POST /orders` | `post:\orders:...` | Forwards body + idempotency key to Process |
| `GET /orders` | `get:\orders:...` | Local order index in Object Store + For-Each fetch |
| `GET /orders/{id}` | maps `toPortalOrder` | 404 if Process returns HTTP:NOT_FOUND |
| `POST /asns` | async accept | **202** — ASN is not fulfillment; it is inbound supply |

## Production notes

- Put **API Manager policies** here (rate limit, client id, JWT).
- Keep payloads small; do not dump WMS bin locations to the browser.
- The in-app order index is a teaching stand-in. Production would query an orders System API or an ODMS with pagination at the source.
