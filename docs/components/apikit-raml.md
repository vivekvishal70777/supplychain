# RAML 1.0 and APIKit

**Files:** `src/main/resources/api/*.raml`, `src/main/mule/apikit-router.xml`

## What it is

RAML is the **contract**. APIKit generates a router that:

1. Validates method, path, headers, and JSON types
2. Dispatches to a flow named `get:\health:config-name` (method + escaped path + config)
3. Returns `APIKIT:BAD_REQUEST` / `NOT_FOUND` / `METHOD_NOT_ALLOWED` when the contract is violated

## Flow naming

APIKit escapes `/` as `\`. Example: `POST /purchase-orders` → `post:\purchase-orders:sc-sys-erp-api-config`.

If you rename a RAML resource and forget the flow, you get a router error at startup or 501.

## Console

`<apikit:console>` is bound to `/console/*`. Disable in prod via YAML.

## Libraries

`libraries/errors.raml` is duplicated per app on purpose for this teaching repo. In an enterprise, publish it once to **Anypoint Exchange** as a RAML fragment and `uses:` it from every API.
