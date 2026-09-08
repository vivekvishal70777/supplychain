# Mule Maven Plugin and multi-module reactor

**Files:** `/pom.xml` (parent), each `*/pom.xml`

## What it is

Mule applications are Maven artifacts with `packaging` **`mule-application`**. The `mule-maven-plugin` (`extensions=true`) teaches Maven how to build a deployable JAR that the runtime understands.

The parent POM is `packaging=pom` and lists five modules. Connector **versions are managed once** in `dependencyManagement` so Experience and Process cannot drift onto different HTTP connector versions.

## Why production teams do this

- One Java / Mule runtime version (`app.runtime` 4.6.9, Java 17)
- CloudHub 2.0 deploy config in `pluginManagement`
- Exchange + MuleSoft releases repositories declared centrally

## Commands

```bash
mvn -pl sc-exp-portal-api -am package   # one app
mvn package                             # all (needs EE)
```

## Studio

Import the parent; Studio discovers modules. Do not flatten everything into one app — API-led independent deployability is the operating model.
