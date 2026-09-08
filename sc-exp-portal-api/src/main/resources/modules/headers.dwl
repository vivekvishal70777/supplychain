%dw 2.0
fun resolveCorrelationId(inbound: String | Null): String =
  if (!isEmpty(inbound)) inbound else uuid()
fun outboundHeaders(correlationId: String): Object =
  { "X-Correlation-Id": correlationId, "Cache-Control": "no-store" }
fun prcHeaders(correlationId: String, idempotencyKey: String | Null = null): Object =
  {
    "X-Correlation-Id": correlationId,
    "Content-Type": "application/json",
    ( "X-Idempotency-Key": idempotencyKey ) if (idempotencyKey != null)
  }
