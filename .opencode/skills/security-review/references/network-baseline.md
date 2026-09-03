# GKE / VPC Network Baseline

Acceptable ports, sources, and exposure by environment. GCP uses **VPC firewall rules** (allow/deny by source range, tag, or service account) rather than security groups; GKE adds Kubernetes `Service` and `Ingress`/`Gateway` exposure and `NetworkPolicy`.

## Ingress Rules

### Never Acceptable

| Rule | Reason |
|------|--------|
| `0.0.0.0/0` on any port other than 443 | Public exposure of non-HTTPS services |
| `0.0.0.0/0` on port 22 | SSH must be restricted to known ranges or reached via IAP |
| `0.0.0.0/0` on database ports (5432, 3306, 6379, 27017) | Databases are never public |
| A `LoadBalancer` Service or Ingress with no authentication in front | Unauthenticated public surface |

### Acceptable Public Ingress

| Port | Use Case | Condition |
|------|----------|-----------|
| 443 (HTTPS) | Public web/API | Only behind the GKE-managed HTTP(S) Load Balancer, ideally with Cloud Armor |
| 80 (HTTP) | Redirect to HTTPS only | Must redirect, not serve content |

### Internal / VPC Ingress

| Port | Use Case | Acceptable Source |
|------|----------|-------------------|
| Application ports | Service-to-service | Specific source service account or a `NetworkPolicy` selector |
| 5432 | Cloud SQL / Postgres | Private Service Connect or authorized networks; app SA only |

## Egress Rules

Most workloads need outbound HTTPS. Default egress to `0.0.0.0/0:443` is acceptable for most services.

| Rule | Concern |
|------|---------|
| `0.0.0.0/0` on all ports | Data-exfiltration risk — scope to needed ports |
| Egress to specific external IPs without explanation | Could be C2 or an unapproved external service |

## Workload Hardening (GKE)

- Pods run as non-root with a read-only root filesystem and dropped Linux capabilities.
- A `NetworkPolicy` restricts pod-to-pod traffic to what the app needs; default-deny where possible.
- Private cluster: nodes have no public IPs; the control plane is on a private or authorized-networks endpoint.
- Workload Identity is enabled so pods authenticate as a dedicated Google service account, not a node key.

## Environment-Specific Rules

### Dev / Staging
- More permissive internal ranges acceptable between non-prod resources
- Still no public database ports, and still no `0.0.0.0/0` on SSH

### Production
- All ingress references a specific source range, tag, or service account — no broad ranges (`/16` or wider) without justification
- Cloud Armor attached to public-facing load balancers
- Access logging enabled on load balancers and on buckets holding sensitive data
