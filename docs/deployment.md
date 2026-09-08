# Deployment and operations

## Environments

| `mule.env` | Config file | Console | Object Store | Typical target |
|---|---|---|---|---|
| `local` | `config-local.yaml` | on | in-memory | laptop |
| `dev` | `config-dev.yaml` | on | persistent | CloudHub 2.0 Design |
| `prod` | `config-prod.yaml` | **off** | persistent | CloudHub 2.0 Production |

Set `mule.env` as an application property in Runtime Manager. Do not bake prod hostnames into `local`.

## CloudHub 2.0

The parent POM contains a `cloudhub2Deployment` skeleton:

- `replicas: 2`
- rolling update
- `enforceDeployingReplicasAcrossNodes: true`
- 0.2 vCores as a starting point (raise Process API first — it is CPU-heavy on DataWeave + HTTP)

Deploy one application at a time, System → Process → Experience. Wire private DNS (`*.internal`) in `config-prod.yaml`.

```bash
mvn -pl sc-sys-erp-api mule:deploy \
  -Danypoint.environment=Production \
  -Dcloudhub2.target=your-private-space
```

## API Manager

1. Publish each RAML to Exchange.
2. Create an API instance in API Manager; copy the **API ID**.
3. Enable autodiscovery (see `api-autodiscovery.xml.example`).
4. Apply policies on the **Experience** instance first: Client ID Enforcement, Rate Limiting, CORS, JWT Validation.
5. Apply spike control on Process if Experience is public.

System APIs should not be internet-facing. Put them on an internal DLB / private space.

## Object Store v2

For CloudHub, switch Object Store config to the CloudHub Object Store v2 REST implementation (connector config `persistent=true` is the local analogue). Idempotency keys must survive a rolling restart.

## Anypoint MQ (production upgrade from VM)

`sc-sys-tms-api` uses **VM queues** so a single replica can demonstrate async tracking. In a cluster, VM is **not** shared. Replace `vm:publish` / `vm:listener` with Anypoint MQ (or JMS) and keep the DLQ pattern.

## SLOs (suggested)

| Probe | Use |
|---|---|
| `GET /health` | Kubernetes / CH2 liveness |
| `GET /ready` | Readiness — Process checks ERP+WMS+TMS |

Alert on:

- 5xx rate at Experience
- `APP:CIRCUIT_OPEN` logs in Process
- DLQ depth on tracking events
- Object Store errors (`OS:*`)

## Secrets

`mule-artifact.json` lists `secureProperties` so Runtime Manager masks them. Encrypt with the Secure Properties tool; never commit `.jks` files (see `.gitignore`).
