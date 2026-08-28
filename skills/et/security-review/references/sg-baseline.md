# Security Group Baseline

Acceptable ports and CIDR ranges by environment.

## Ingress Rules

### Never Acceptable

| Rule | Reason |
|------|--------|
| `0.0.0.0/0` on any port other than 443 | Public exposure of non-HTTPS services |
| `0.0.0.0/0` on port 22 | SSH must be restricted to known CIDRs or accessed via SSM |
| `0.0.0.0/0` on port 3389 | RDP must never be publicly exposed |
| Any ingress on database ports (3306, 5432, 1433, 27017) from `0.0.0.0/0` | Databases are never public |

### Acceptable Public Ingress

| Port | Use Case | Condition |
|------|----------|-----------|
| 443 (HTTPS) | Public web services | Only behind ALB/CloudFront with WAF |
| 80 (HTTP) | Redirect to HTTPS only | Must redirect, not serve content |

### Internal / VPC Ingress

| Port | Use Case | Acceptable Source |
|------|----------|-------------------|
| 443 | Service-to-service | Specific security group ID or VPC CIDR |
| Application ports | Microservices | Specific security group of the caller |
| 5432/3306 | Database | Application security group only |

## Egress Rules

### Default Acceptable

Most services need outbound HTTPS. A default egress of `0.0.0.0/0:443` is acceptable for most workloads.

### Flag for Review

| Rule | Concern |
|------|---------|
| `0.0.0.0/0` on all ports | Data exfiltration risk — scope to needed ports |
| Egress to specific IPs without explanation | Could be C2 or unauthorized external services |

## Environment-Specific Rules

### Sandbox/Dev
- More permissive CIDR ranges acceptable between sandbox resources
- Still no public database ports
- Still no `0.0.0.0/0` SSH/RDP

### Production
- All ingress must reference specific security groups or documented CIDRs
- No broad CIDR ranges (/16 or wider) unless ASU campus ranges
- Access logging enabled on all ALBs
- WAF attached to public-facing ALBs

## ASU Campus CIDRs

When restricting to "ASU only," reference the `module-asu-ips` and `module-vendor-ips` modules rather than hardcoding IPs. These IPs rotate — hardcoded values will go stale.

```hcl
module "asu_ips" {
  source = "jfrog-cloud.devops.asu.edu/asu-terraform-modules__dco-terraform/asu-ips/null"
}
```
