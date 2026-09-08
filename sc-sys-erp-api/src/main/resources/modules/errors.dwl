%dw 2.0
/**
 * Canonical error payload used by every API in this platform.
 * Import: import * from modules::errors
 */
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
    case "APIKIT:NOT_ACCEPTABLE" -> 406
    case "APIKIT:UNSUPPORTED_MEDIA_TYPE" -> 415
    case "HTTP:TIMEOUT" -> 504
    case "HTTP:CONNECTIVITY" -> 503
    case "APP:NOT_FOUND" -> 404
    case "APP:CONFLICT" -> 409
    case "APP:VALIDATION" -> 422
    case "APP:CREDIT_HOLD" -> 422
    case "APP:BACKORDER" -> 409
    case "APP:CIRCUIT_OPEN" -> 503
    else -> 500
  }
