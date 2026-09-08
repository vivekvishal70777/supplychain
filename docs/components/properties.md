# Properties and mule.env

**Files:** `application.properties` (`mule.env=local`) + `config/config-{env}.yaml`

## What it is

`${mule.env}` is interpolated by `<configuration-properties file="config/config-${mule.env}.yaml"/>` in `global.xml`.

YAML trees become dotted properties: `sys.erp.host`, `http.port`.

## Rules

- **Never** put secrets in `config-local.yaml` committed to git.
- Prod `http.port` on CloudHub is typically `8081` (platform injects the port). Local uses distinct ports so five apps can co-exist.
- `apikit.consoleEnabled` is `false` in prod — the console is an attack surface.

## Override order (simplified)

Runtime Manager / JVM `-M-Dhttp.port=8099` overrides the file. Use that for port clashes, not a code change.
