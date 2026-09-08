# System API — WMS (`sc-sys-wms-api`)

**Port (local):** 8092  
**Seed data:** `data/inventory.json`, `warehouses.json`

## What it is

Warehouse Management System facade: **on-hand vs allocated vs available**, multi-warehouse, allocation and release.

## Allocation algorithm (simplified)

For each line, take `min(requested, available)` at `warehouseId` default `WH-CHI`.

- All lines zero allocated → `APP:BACKORDER`
- Some shortfall → status `PARTIAL`
- Else `ALLOCATED`

Inventory rows are updated in Object Store so a second order sees reduced availability — useful when you demo two Postman calls.

## Production notes

Real WMS allocation is usually a single atomic API (Manhattan, SAP EWM). Keep **release** as a first-class resource; Process compensation depends on it. Never allocate inside the Experience API.
