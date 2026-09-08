# Scheduler

**Where:** Process `scheduler-inventory-heartbeat`

## What it is

A flow source that fires on `fixed-frequency` or `cron`. Used for reconciliation, watermark polls, cache warm-up.

This repo logs WMS warehouse counts every 15 minutes (`startDelay` 2 minutes so apps can boot).

## Production notes

- Cluster: **all replicas** fire unless you use a cluster-aware lock (Object Store `os:store` with fail-on-exists, or a scheduler on a single worker).
- Prefer Anypoint Scheduler / cron aligned to warehouse cut-off times (`0 0 2 * * ?` for 02:00 DC time).
- Never use a 1ms scheduler to seed data.
