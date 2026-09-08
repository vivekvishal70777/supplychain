# Choice router

**Where:** almost every `implementation.xml`

## What it is

If/else for Mule. First matching `<when expression="...">` wins; optional `<otherwise>`.

## Supply-chain uses in this repo

- Seed Object Store only when `os:contains` is false
- Replay vs create on idempotency hit
- Blocked customer vs continue
- Empty inventory → raise `APP:NOT_FOUND`

Expressions are DataWeave inside `#[ ]`. Keep them side-effect free; put HTTP calls **outside** Choice, then branch on the result.
