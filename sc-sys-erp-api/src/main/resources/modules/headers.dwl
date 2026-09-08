%dw 2.0
/**
 * Correlation and outbound HTTP header helpers.
 */
fun resolveCorrelationId(inbound: String | Null): String =
  if (!isEmpty(inbound)) inbound else uuid()

fun outboundHeaders(correlationId: String): Object =
  {
    "X-Correlation-Id": correlationId,
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff"
  }
