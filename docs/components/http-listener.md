# HTTP Listener

**Files:** `global.xml` (`http:listener-config`), `apikit-router.xml` (`http:listener`)

## What it is

The inbound connector. One `listener-config` (host/port) and many listeners (`/api/*`, `/console/*`).

## Response vs error-response

```xml
<http:response statusCode="#[vars.httpStatus default 200]">
  <http:headers>#[vars.outboundHeaders]</http:headers>
</http:response>
<http:error-response statusCode="#[vars.httpStatus default 500]">
```

The **error-response** block is what the client sees after the global error handler. If you forget it, clients get a generic Mule 500 HTML/text payload instead of your JSON error contract.

## Path

`path="/api/*"` plus RAML `baseUri` versioning: keep version in the RAML `version: v1` and optionally prefix `/api/v1` when you introduce breaking changes. This repo uses `/api` for local simplicity.
