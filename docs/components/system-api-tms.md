# System API — TMS (`sc-sys-tms-api`)

**Port (local):** 8093  
**Async:** `vm:queues` `tracking-events` and `tracking-events-dlq`

## What it is

Transportation Management facade: carrier catalog, book a shipment, ingest tracking events.

## Booking

If `carrierId` is omitted, the first active **PARCEL** carrier is chosen (UPS in seed data). ETA is SLA hours adjusted by service level (`OVERNIGHT` / `EXPEDITED` / `STANDARD`).

## Async tracking

`POST /shipments/{id}/events` returns **202** immediately after `vm:publish`. A separate flow `tracking-event-consumer` updates the shipment status. Failures are published to the DLQ (`on-error-continue`).

That is the same shape you will use with Anypoint MQ in a multi-replica CloudHub app: HTTP ack + worker + DLQ.

## Production notes

Carrier webhooks are abusive (retries, duplicates). Combine this VM pattern with **idempotency** on `eventType + occurredAt + shipmentId`.
