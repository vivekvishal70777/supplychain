%dw 2.0
/**
 * Experience-layer reshaping: process canonical -> portal UX model.
 */
var statusLabels = {
  RECEIVED: "Received",
  CREDIT_HOLD: "On credit hold",
  BACKORDER: "Backordered",
  ALLOCATED: "Inventory reserved",
  BOOKED: "Shipped / in transit",
  CANCELLED: "Cancelled",
  FAILED: "Failed"
}

fun toPortalOrder(f: Object) = {
  orderId: f.fulfillmentId,
  status: f.status,
  statusLabel: statusLabels[f.status] default f.status,
  customerId: f.customerId,
  tracking: f.trackingNumber,
  summary: (f.statusLabel default statusLabels[f.status] default f.status) ++ " · " ++ (f.poId default ""),
  createdAt: f.createdAt,
  poId: f.poId,
  shipmentId: f.shipmentId,
  totals: f.totals
}

fun stockHealth(available: Number, safety: Number = 0) =
  if (available <= 0) "STOCKOUT"
  else if (available < safety) "LOW"
  else "HEALTHY"
