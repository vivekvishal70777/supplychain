# Flow-ref and sub-flows

**Where:** `impl-ensure-seed`, `impl-orchestrate-fulfillment`, compensation sub-flows

## What it is

`<flow-ref name="..."/>` calls another flow or sub-flow in-process (no serialization).

- **sub-flow:** no source, inherits the caller’s error handler unless a `try` wraps the ref
- **flow:** may have its own source (HTTP, VM, Scheduler) and error handler

## Design rule

Put reusable steps (seed, circuit check, compensate) in **sub-flows**. Keep APIKit-generated names as thin wrappers that set variables then `flow-ref` the implementation. That makes MUnit mocking (`munit:spy` / mock `flow-ref`) tractable.
