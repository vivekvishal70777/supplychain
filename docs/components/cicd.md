# CI/CD

**Files:** `.github/workflows/ci.yml`, `scripts/validate-artifacts.py`, parent POM deploy plugin

## Pipeline stages (intended)

1. **PR** — `python scripts/validate-artifacts.py` (XML well-formed, JSON, YAML, RAML header). Runs without Mule EE.
2. **MUnit** — `mvn test` on a licensed runner.
3. **Deploy** — `mule-maven-plugin` CloudHub 2.0 to Design, then Production after approval.

## Why split validation

Most GitHub-hosted runners will not have a Mule EE license. Contract and well-formedness checks still catch broken XML before a reviewer opens Studio.

Promote artifacts **per application**, System first, matching [deployment.md](../deployment.md).
