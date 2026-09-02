# 0006 — Edge SSO with backend JWT validation

Status: Accepted
Date: 2026 (hackathon planning)

## Context

The prototype is deployed to a dev GKE cluster. Unauthenticated endpoints would let anyone
who can reach the service start Runs (spending the provider budget) and read or export
datasets. The team operates Cloudflare Enterprise and manages it with Terraform, and can place
the application behind Cloudflare Access (Zero Trust) restricted to asu.edu SSO. The
Cloudflare / GKE / Terraform specifics are being planned in a separate session; only the
application-boundary contract is decided here.

## Decision

1. **Edge authentication**: the application sits behind **Cloudflare Access restricted to
   asu.edu SSO**. Unauthenticated traffic never reaches the backend in normal operation.
2. **Defense in depth**: the FastAPI backend **validates the signed Access JWT itself** on
   every request — verifying the signature against the proxy's JWKS, the audience, and the
   asu.edu identity claim — via an injected auth dependency. The backend does not blindly trust
   that the edge proxy is in front (guards against misconfigured ingress or in-cluster
   callers).
3. **Authorization (prototype)**: any authenticated asu.edu principal is authorized. No finer
   RBAC yet.
4. **Principal capture**: the authenticated identity is surfaced through the auth seam so
   Experiments and Runs can gain per-user ownership later without refactoring.
5. The provider API key is a **server-side secret only**, never sent to the frontend.

## Consequences

- Two independent layers (edge SSO + backend JWT verification) must both pass, so a single
  misconfiguration does not expose the API.
- The prototype has no per-user data isolation yet, but the principal is available to add it.
- Infra details (Cloudflare Access config, JWKS/audience values, GKE ingress, Terraform) are
  deferred to the separate infrastructure planning session.

## Alternatives considered

- **No in-app auth, edge-only trust** — earlier prototype option; rejected because it leaves
  the backend open to any in-cluster or misrouted caller and risks provider-budget abuse.
- **GCP Identity-Aware Proxy (IAP)** — a viable Google-native edge, but the team already
  operates Cloudflare Enterprise via Terraform; IAP noted as an alternative in the GCP service
  mapping.
