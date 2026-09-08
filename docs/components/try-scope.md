# Try scope and on-error-continue

**Where:** circuit retrieve, compensation HTTP, tracking consumer, Experience order index

## What it is

`<try>` attaches a local error handler.

- `on-error-propagate` — map or enrich, then still fail the parent
- `on-error-continue` — swallow, optionally set a default (empty index, empty circuit)

## Compensation example

Cancel-PO HTTP is wrapped in `on-error-continue` so a **secondary** failure during rollback is logged but does not hide the original allocation error. You still raise `APP:BACKORDER` after compensation is attempted.

That is operationally honest: the customer sees allocation failure; ops sees a compensation log line to repair.
