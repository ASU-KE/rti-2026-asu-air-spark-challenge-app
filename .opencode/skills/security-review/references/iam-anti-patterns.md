# GCP IAM Anti-Patterns

Common over-permissive patterns, with fixes. GCP IAM grants a **role** (a bundle of permissions) to a **member** (user, group, or service account) on a **resource** (organization, project, or a single resource).

## 1. Primitive Roles

**Bad:** granting a project-wide primitive role.

```hcl
resource "google_project_iam_member" "app" {
  project = var.project_id
  role    = "roles/editor"        # or roles/owner, roles/viewer
  member  = "serviceAccount:${google_service_account.app.email}"
}
```

Primitive roles (`roles/owner`, `roles/editor`, `roles/viewer`) span every service in the project.

**Fix:** grant a predefined role scoped to the service the workload actually uses:

```hcl
resource "google_project_iam_member" "app" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.app.email}"
}
```

## 2. Using the Default Compute Service Account

**Bad:** workloads run as the default compute service account, which carries broad editor-like scope.

**Fix:** create a dedicated least-privilege service account per workload and bind only the roles it needs. Disable automatic role grants to the default SA.

## 3. Exported Service-Account Keys

**Bad:**
```hcl
resource "google_service_account_key" "app" {
  service_account_id = google_service_account.app.name
}
```

Exported JSON keys are long-lived credentials that leak and never expire on their own.

**Fix:** use **Workload Identity Federation** — bind the GKE Kubernetes service account (or external CI/CD identity) to the Google service account, so no key material exists:

```hcl
resource "google_service_account_iam_member" "wi" {
  service_account_id = google_service_account.app.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[${var.k8s_namespace}/${var.k8s_sa}]"
}
```

## 4. Public Members (`allUsers` / `allAuthenticatedUsers`)

**Bad:**
```hcl
resource "google_storage_bucket_iam_member" "public" {
  bucket = google_storage_bucket.data.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"                 # anyone on the internet
}
```

`allAuthenticatedUsers` is barely better — it means any Google account, not your users.

**Fix:** grant to the specific service account, group, or domain that needs access. Reserve `allUsers` for genuinely public assets (e.g. a static site bucket), and document why.

## 5. Project-Level Binding for a Single-Resource Need

**Bad:** granting `roles/storage.admin` at the project when the workload touches one bucket.

**Fix:** grant on the resource, not the project:

```hcl
resource "google_storage_bucket_iam_member" "app" {
  bucket = google_storage_bucket.uploads.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.app.email}"
}
```

## 6. Unscoped Impersonation (`actAs`)

**Bad:** granting `roles/iam.serviceAccountUser` or `roles/iam.serviceAccountTokenCreator` at the project level lets a member impersonate every service account.

**Fix:** grant impersonation on the specific target service account only, and only where a workflow genuinely needs to act as it.

## 7. "We'll Scope Down Later"

Any comment or PR description saying permissions will be tightened in a future PR is a red flag. Temporary permissions become permanent. Require scoping now, or a linked follow-up ticket with a deadline.
