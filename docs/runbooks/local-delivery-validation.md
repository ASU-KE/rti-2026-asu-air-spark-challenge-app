# Local delivery validation

This runbook runs application checks, validates Cloud Build policy, and renders the development Kubernetes overlay as parseable YAML for repository-specific policy checks. It does not contact Google Cloud or a Kubernetes API server and does not perform Kubernetes/OpenAPI or CRD schema validation.

## Prerequisites

- Node.js 24.8 or later in the Node 24 release line, or Node.js 26, and npm 11. The compiled API surface is constrained by Node 24 type definitions; declared Cloud Build and container execution use Node 24.8.
- `kubectl` with Kustomize support, or standalone `kustomize`.
- Docker only for image build and runtime smoke checks. Start the local Docker daemon before those checks.

## Deterministic validation

From the repository root:

```bash
npm ci
npm run validate
npm run validate:delivery
```

`validate` verifies the byte-preserved inactive vendor snapshot separately and excludes that intentionally unchanged template from active source vulnerability scanning. `validate:delivery` performs these local-only checks:

1. Parses both Cloud Build YAML files and verifies the PR/main authority split.
2. Rejects mutable tags, build-time secrets, IAM mutation, PR publication, and PR cloud/cluster commands.
3. Renders the dev Kustomize overlay with a non-deployable fixture digest.
4. Parses every rendered YAML document and enforces the repository's namespace, hardening, probe, resource, autoscaling, disruption-budget, Managed Prometheus, immutable-image, and NetworkPolicy assertions. These are policy checks, not full Kubernetes or CRD schema validation.
5. Syntax-checks the shell scripts. It does not run `gcloud`, `kubectl apply`, or any remote command.

To inspect a non-deployable rendered fixture:

```bash
node scripts/ci/render-kubernetes.mjs \
  --imageRef us-west4-docker.pkg.dev/asu-ke-rto-web-svcs/validation-fixture/rti-air-spark@sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa \
  --serviceVersion validation-fixture \
  --otlpEndpoint http://collector.observability.svc.cluster.local:4318 \
  --otlpNamespace observability \
  --otlpAppLabel otel-collector
```

The renderer rejects other projects or regions, mutable image references, invalid labels, credential-bearing collector URLs, and unresolved placeholders.

## Container validation

When Docker is running:

```bash
docker build --tag rti-air-spark:local .
scripts/ci/smoke-container.sh rti-air-spark:local
```

The smoke script verifies the image-declared non-root user and runs with a read-only root filesystem, bounded `/tmp` tmpfs, no new privileges, and all capabilities dropped. It checks `/health/live`, `/health/ready`, `/api/v1/status`, `/metrics`, and `/`, then removes the container.

## Intentionally unavailable locally

The repository does not use `gcloud builds submit` as a configuration validator because the command has no `--dry-run` or `--validate-only` option and would create remote build state. Local rehearsal also excludes trigger creation, credential acquisition, Artifact Registry push, `kubectl apply`, IAM/RBAC changes, namespace creation, secret changes, dashboards, and alert policies.

The placeholder builder images in both Cloud Build files make the configurations fail closed until a human approves and pins the delivery toolchain described in [human-gated deployment prerequisites](human-gated-deployment-prerequisites.md).
