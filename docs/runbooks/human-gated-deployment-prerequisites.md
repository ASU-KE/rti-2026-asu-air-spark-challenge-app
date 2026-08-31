# Human-gated deployment prerequisites

This checklist identifies state that must be approved and provisioned separately before either Cloud Build trigger is enabled. It is not an executable bootstrap guide and authorizes no cloud or cluster mutation.

## Decisions still required

- Artifact Registry repository name, tag immutability policy, cleanup policy, and final `_IMAGE_URI`.
- Exact PR validation and merged-main deploy service-account emails and trigger names.
- Digest-pinned Docker, Trivy, validation, and GKE deploy builder images. The validation image must contain Node.js 24.8 or later in the Node 24 release line plus `kubectl`/Kustomize; the deploy image must also contain `gcloud` and support internal GKE credentials.
- Private Cloud Build worker pool and verified network path to the private GKE control plane.
- Approved OTLP HTTP/protobuf collector origin, namespace, workload label, and whether port 4318 is correct.
- Approved first-deployment rollback digest under the final `_IMAGE_URI`.
- SBOM/scan evidence storage, retention, and access controls.
- Runtime secret design if the selected product later consumes ASU RC credentials. No runtime secret is declared by the neutral scaffold.
- Dashboard queries, alert thresholds, notification channels, and evidence retention.

## Identity and authority boundaries

### PR validation identity

The PR trigger must use a dedicated user-managed service account. It needs only build execution/logging and read access to approved private builder images, if used. It must not have Artifact Registry write, Secret Manager access, GKE credential acquisition, Kubernetes RBAC, IAM mutation, or runtime-secret access.

### Merged-main deploy identity

The main trigger must use a different user-managed service account. Grant only the permissions required to write/read the approved Artifact Registry repository, write build logs/evidence, and call `container.clusters.get` for the fixed cluster. Bind its Kubernetes identity only in `rti-air-spark-dev` and only to the namespaced resource kinds used by the rendered manifest. It must not create namespaces, cluster roles, IAM bindings, secrets, DNS, TLS, or monitoring infrastructure.

### Runtime identity

The workload uses a dedicated Kubernetes ServiceAccount with `automountServiceAccountToken: false`; the Pod repeats that setting. Do not annotate it with a Google service account until the selected application has an approved Google API permission. Never use a service-account key file.

## Platform prerequisites

A human must verify and record:

- The namespace already exists and its owners approve this workload.
- The Artifact Registry repository exists in `us-west4`, the trigger identities have the reviewed repository-level roles, and image cleanup cannot remove the active/rollback digests.
- The private worker pool can reach the cluster internal endpoint and DNS.
- The `monitoring.googleapis.com/v1` `PodMonitoring` CRD and Managed Service for Prometheus collection are available without changing cluster monitoring settings.
- NetworkPolicy is enforced. The real DNS implementation matches the `kube-system`/`k8s-app=kube-dns` policy, and Managed Prometheus collectors originate from `gmp-system`.
- The approved OTLP collector selectors match `networkpolicy-allow-otlp.yaml`; its Google export identity has only `roles/serviceusage.serviceUsageConsumer` and `roles/telemetry.writer` at the approved scope.
- Two replicas, the PDB, and HPA fit available cluster capacity. Initial `100m/128Mi` requests, `500m/512Mi` limits, HPA range 2–4, and 70% CPU target are event defaults to tune with evidence.
- No ingress, DNS, TLS, Cloud Armor, public endpoint, or runtime secret is assumed by this configuration.

## Trigger controls

Configure the PR trigger to use `cloudbuild.pr.yaml` and the validation identity. Configure the trusted push-to-`main` trigger to use `cloudbuild.main.yaml` and the deploy identity. Trigger substitutions must replace every `REQUIRED` or all-zero placeholder. Do not allow pull-request content to choose project, identity, builder image, scanner policy, cluster, namespace, image repository, collector, or rollback digest.

Before any future `gcloud` command, follow this gate:

- **Step 1**: Syntax Validation via `gcloud help <leaf_command>`
- **Step 2**: Parameter Verification (confirming required and optional flags, and explicitly checking if the `--dry-run` or `--validate-only` flag is supported)
- **Step 3**: Dry-Run Command Proposal (If `--dry-run` or `--validate-only` is supported, there MUST be a `--dry-run` or `--validate-only` invocation before the next step.)
- **Step 4**: Command Proposal & Authorization (If the command is on the "Prohibited Operations" denylist, state that autonomous execution is forbidden, and the user MUST be explicitly asked for authorization to proceed. If the command is NOT on the denylist, propose or proceed with execution, while following all execution constraints.)

IAM/RBAC changes, trigger creation, repository creation, namespace changes, monitoring enablement, secrets, and live deployment remain Human-Gated Actions requiring a separate exact proposal and explicit approval.
