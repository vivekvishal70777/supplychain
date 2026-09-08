# Secure configuration properties

**Example:** `sc-exp-portal-api/src/main/resources/examples/secure-properties.xml.example`

## What it is

Values encrypted with AES and decrypted at boot with `key="${secure.key}"`. YAML file `config/secure-prod.yaml` holds `![string] "encrypted..."`.

The **key** comes from Runtime Manager / a secrets manager, never from git.

## Why the example is not active

A missing keystore/key would prevent local startup. Copy the example into `src/main/mule` only when `secure.key` is injected.

Pair with `mule-artifact.json` `secureProperties` so even decrypted-at-runtime names are masked in the control plane UI.

`.gitignore` excludes `*.jks` and `**/secrets/**`.
