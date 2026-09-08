%dw 2.0
fun errorPayload(correlationId: String, status: Number, errorCode: String, message: String, details: Any = null) = {
  correlationId: correlationId,
  timestamp: now(),
  status: status,
  errorCode: errorCode,
  message: message,
  (details: details) if (details != null)
}

fun httpStatusFromError(errorType: String): Number =
  errorType match {
    case "APIKIT:BAD_REQUEST" -> 400
    case "APIKIT:NOT_FOUND" -> 404
    case "APIKIT:METHOD_NOT_ALLOWED" -> 405
    case "HTTP:TIMEOUT" -> 504
    case "HTTP:CONNECTIVITY" -> 503
    case "APP:NOT_FOUND" -> 404
    case "APP:CONFLICT" -> 409
    case "APP:VALIDATION" -> 422
    case "APP:BACKORDER" -> 409
    else -> 500
  }
