%dw 2.0
/**
 * Maps scatter-gather / system payloads into the fulfillment canonical order.
 */
fun creditOk(customer: Object): Boolean =
  customer.status == "ACTIVE" and (customer.openPayables.amount default 0) < (customer.creditLimit.amount default 0)

fun fulfillmentStatus(creditHold: Boolean, allocationStatus: String, booked: Boolean): String =
  if (creditHold) "CREDIT_HOLD"
  else if (allocationStatus == "BACKORDER") "BACKORDER"
  else if (booked) "BOOKED"
  else if (allocationStatus == "ALLOCATED" or allocationStatus == "PARTIAL") "ALLOCATED"
  else "RECEIVED"
