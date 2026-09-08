# mule-artifact.json

**Files:** each module’s `mule-artifact.json`

## What it is

Descriptor the Mule runtime reads from the application JAR:

- `minMuleVersion` — refuse to start on an older runtime
- `javaSpecificationVersions` — Java 17
- `secureProperties` — property names Runtime Manager must mask in logs and UI

## Why it matters

If you put `https.keystore.password` in YAML but forget `secureProperties`, support staff (and log aggregators) can see it. Listing the key here is a **platform contract**, not encryption by itself.

This repo lists `anypoint.platform.client_secret`, `https.keystore.password`, and `secure.key`.
