# Raise-error

**Where:** Choice branches across System and Process APIs

## What it is

```xml
<raise-error type="APP:NOT_FOUND" description="#['Customer ' ++ id ++ ' not found']"/>
```

Creates a custom namespace `APP` (you do not register it). The global error handler matches `APP:NOT_FOUND`.

## Why not HTTP status in the middle of a flow

Keep business errors **typed** until the listener boundary. Then one handler owns JSON shape. Otherwise every flow invents a different 404 body.

Use `description` for operators; the Process handler may replace it with a generic message for 5xx.
