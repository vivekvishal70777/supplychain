# MUnit

**Files:** `src/test/munit/*.xml` in each module

## What it is

Mule’s unit/integration test framework (EE). Tests here lock **DataWeave business rules** (credit, stock health, HTTP status mapping) so they run without HTTP stubs.

## What you should add next

- `munit:spy` on `http:request` in Process to assert compensation is called when TMS is mocked to fail
- Listener-level tests with `munit-tools:http` if you add the test HTTP requester pattern

MUnit is skipped in the default GitHub Action unless `MULE_EE_AVAILABLE=true` and Anypoint credentials are present.
