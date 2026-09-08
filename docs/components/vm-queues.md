# VM connector, queues, and DLQ

**Where:** TMS `global.xml` + `tracking-event-consumer`

## What it is

In-process (or persistent file-backed) queues. `vm:publish` from the HTTP flow; `vm:listener` consumes.

```
HTTP 202  →  tracking-events  →  consumer updates shipment
                 │ on failure
                 ▼
           tracking-events-dlq
```

## Why a DLQ

Poison messages (unknown shipment id, bad JSON) must not block the main queue. Operations replay from the DLQ after a fix.

## Cluster limitation

VM queues are **not** shared across CloudHub replicas. Production tracking should use **Anypoint MQ** with a DLQ exchange. The flow shape stays the same: publish → listener → try → DLQ.
