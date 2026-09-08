# Async scope

**Where:** Experience `POST /asns`

## What it is

`<async>` copies the event and continues the caller immediately. The inner processors run on another thread.

Used for ASN **202 Accepted**: the portal should not wait for warehouse inbound processing.

## Watch-outs

- Errors inside async do **not** fail the HTTP response (already sent). Log them and send to a queue/DLQ.
- Not a substitute for VM/MQ when you need durability — async is in-memory. Pair with Object Store write **before** async (this repo stores the ASN first).
