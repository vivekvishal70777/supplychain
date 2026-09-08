# For-Each

**Where:** Process availability check; Experience `GET /orders` paging

## What it is

Iterates a collection, setting `payload` to each element. Variables you set inside persist (with last-write-wins unless you accumulate, as Experience does with `vars.items`).

## Watch-outs

- Sequential by default — N HTTP calls for N SKUs. For 50 SKUs use Scatter-Gather with a max concurrency or a WMS bulk API.
- After For-Each, `payload` is the **original collection**, not the last item. That is why we accumulate into `vars.checked` / `vars.items`.

This repo’s availability For-Each is intentionally simple so you can see the pattern; a production WMS should expose `POST /inventory/query` in bulk.
