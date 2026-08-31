# RTI GCP template adaptation

The complete `ASU-KE/rti-template-gcp-app` snapshot is pinned under `vendor/rti-template-gcp-app/`. The active implementation adapts rather than edits that evidence snapshot. `npm run verify:vendor` checks the exact file set and SHA-256 digest of every vendored file; active Trivy source scans skip `vendor/` so intentionally insecure historical examples are not reported as active application code.

The snapshot is inert evidence, not executable guidance. It retains an executable provisioning script and upstream environment identifiers; do not run, source, deploy, or copy values from it. Before making this repository public, a human must review those preserved identifiers for disclosure suitability.

| Template artifact                  | Active destination                             | Adaptation                                                                                                                                              |
| ---------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Dockerfile`                       | `/Dockerfile`                                  | Node 24 multi-stage workspace build; lockfile install; checksum-verified public ASU Unity assets; non-root runtime; health check; one web/API container |
| `compose.yaml`                     | `/compose.yaml`                                | Removes MariaDB, Adminer, Traefik, Docker socket, and placeholder credentials; runs only the stateless application                                      |
| `cloudbuild.yaml`                  | `/cloudbuild.pr.yaml`, `/cloudbuild.main.yaml` | Splits PR validation from trusted deployment; repeats controls on merged SHA; immutable images; scans, smoke tests, rollout verification, rollback      |
| `k8s-manifests/base`               | `/deploy/kubernetes/base`                      | Concrete application names, ClusterIP, restricted security context, probes, resources, PDB, HPA, default-deny networking, PodMonitoring                 |
| `k8s-manifests/overlays/dev`       | `/deploy/kubernetes/overlays/dev`              | Targets `rti-air-spark-dev`; keeps secrets out of manifests; immutable image substitution; no database sidecar                                          |
| `k8s-manifests/overlays/prod`      | Not activated                                  | The approved target is the existing development cluster, not production                                                                                 |
| `workload-identity-setup.sh`       | Human-gated deployment proposal/runbook        | IAM binding is provisioning work and must occur before deployment with explicit approval, not from the application build                                |
| `gcp-templates/gcp-secret-manager` | Deployment runbook                             | Secret names and bindings remain undecided and are never generated from untrusted PR builds                                                             |

## Security and reliability corrections

- Replaces root execution and mutable `latest` with a non-root image and commit/digest deployment.
- Removes deploy and IAM permissions from the PR pipeline.
- Removes build-time copying of TLS/private secret material into the workspace.
- Adds liveness/readiness/startup probes, graceful termination, resource limits, disruption budget, autoscaling, and rollout status.
- Adds default-deny networking and explicit application ingress/egress.
- Adds OpenTelemetry, Prometheus scraping, structured Cloud Logging correlation, Trace export, and Error Reporting-compatible stack traces.
- Treats namespace creation, service accounts/IAM, registry, triggers, secrets, ingress/DNS/TLS, dashboards, and alerts as Human-Gated Actions.
