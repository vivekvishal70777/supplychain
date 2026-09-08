%dw 2.0
fun resolveCorrelationId(inbound: String | Null): String =
  if (!isEmpty(inbound)) inbound else uuid()
fun outboundHeaders(correlationId: String): Object =
  { "X-Correlation-Id": correlationId, "Cache-Control": "no-store" }
