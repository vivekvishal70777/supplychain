# log4j2

**Files:** `src/main/resources/log4j2.xml`

## What it is

Mule’s logging implementation. This repo uses a console `PatternLayout` with `correlation=%X{correlationId}`.

ERP’s file also defines a `JsonLayout` appender you can switch the root to in prod (`logging.json: true` is a YAML flag you can wire to a property lookup if you add a custom filter).

## Production

- JSON logs to stdout for CloudHub / RTF log drain
- Never log payloads containing PAN, addresses beyond policy, or auth headers
- Set `org.mule.runtime.core.internal.processor.LoggerMessageProcessor` to INFO, not DEBUG, in prod
