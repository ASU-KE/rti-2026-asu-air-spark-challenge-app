# Deployment rehearsal and rollback

This runbook explains the trusted merged-`main` pipeline. It is a review and dry-render procedure, not authorization to submit a build or mutate the cluster.

## Fixed target

- Project: `asu-ke-rto-web-svcs`
- Region and GKE location: `us-west4`
- Cluster: `websvcs-gke-private-dev`
- Namespace: `rti-air-spark-dev`
- Deployment, Service, and container: `rti-air-spark`

`guard-cloudbuild.mjs` rejects any different target before build, publication, credential acquisition, or deployment.

## Main pipeline graph

1. Verify the fixed target and all approved digest-pinned builder substitutions.
2. Install from `package-lock.json`; run formatting, lint, typechecks, tests, and builds.
3. Audit production dependencies and scan source, configuration, and secrets at High/Critical severity.
4. Render the Kubernetes manifests and check the repository policy baseline (not Kubernetes/OpenAPI or CRD schema validation).
5. Build the merged commit as `${_IMAGE_URI}:$COMMIT_SHA`; scan it and generate a CycloneDX SBOM.
6. Push only the commit tag, then resolve the registry's canonical digest with `gcloud artifacts docker images describe`. Deployment never uses the tag.
7. Acquire short-lived credentials for the fixed private regional cluster with `gcloud container clusters get-credentials --internal-ip --location=us-west4 --project=asu-ke-rto-web-svcs --quiet`.
8. Render the candidate and identify the currently deployed digest. If a deployment exists, capture all 11 live app resources named by the candidate, reject an incomplete snapshot, remove server-managed fields, and verify that the captured Deployment uses that digest. Stop before mutation if this full known-good snapshot cannot be created.
9. On an empty namespace, deploy and smoke the separately approved bootstrap digest first, remove partial bootstrap resources on failure, and capture the verified bootstrap configuration before attempting the candidate.
10. Apply the candidate resources, wait up to five minutes for rollout, and smoke the ClusterIP Service through temporary port-forwarding.
11. If apply, rollout, or smoke fails, apply the captured full known-good configuration and digest, verify rollout and smoke again, report whether rollback converged, and fail the build. The workflow never uses unbounded `kubectl rollout undo`.

## Rehearsal checklist

- Run the commands in [local delivery validation](local-delivery-validation.md).
- Review the rendered fixture and confirm it has no `Namespace`, `Secret`, `Ingress`, cluster-scoped RBAC, mutable image tag, or unresolved placeholder.
- Review `cloudbuild.main.yaml` substitutions against the approved prerequisite record.
- Confirm the deploy service account has no IAM administration and Kubernetes RBAC is namespace-scoped.
- Confirm the approved rollback image is a digest under the same `_IMAGE_URI`.
- Confirm the private worker pool can reach the cluster's internal endpoint.
- Confirm Managed Service for Prometheus, NetworkPolicy enforcement, DNS selectors, and the OTLP collector selectors on the actual cluster before enabling the trigger.

## Future `gcloud` execution gate

- **Step 1**: Syntax Validation via `gcloud help <leaf_command>`
- **Step 2**: Parameter Verification (confirming required and optional flags, and explicitly checking if the `--dry-run` or `--validate-only` flag is supported)
- **Step 3**: Dry-Run Command Proposal (If `--dry-run` or `--validate-only` is supported, there MUST be a `--dry-run` or `--validate-only` invocation before the next step.)
- **Step 4**: Command Proposal & Authorization (If the command is on the "Prohibited Operations" denylist, state that autonomous execution is forbidden, and the user MUST be explicitly asked for authorization to proceed. If the command is NOT on the denylist, propose or proceed with execution, while following all execution constraints.)

The leaf help for `gcloud builds submit` was checked while authoring this runbook. It exposes neither `--dry-run` nor `--validate-only`; therefore it is not a local validation mechanism. A future submission must be proposed separately with explicit project, region, configuration, service account, and substitutions, then explicitly authorized. No build was submitted while creating this runbook.
