# Least-privilege GCP IAM starting point.
# Grant a specific role to a dedicated service account at the narrowest scope.
# Replace ROLE and the resource binding with the minimum the workload needs.

resource "google_service_account" "workload" {
  project      = var.project_id
  account_id   = "svc-EXAMPLE-workload"
  display_name = "Least-privilege SA for EXAMPLE workload"
}

# Prefer a resource-level binding over a project-level one.
resource "google_storage_bucket_iam_member" "workload" {
  bucket = google_storage_bucket.example.name
  role   = "roles/storage.objectViewer" # scope to the actions actually needed
  member = "serviceAccount:${google_service_account.workload.email}"
}

# Use Workload Identity Federation instead of exported service-account keys.
resource "google_service_account_iam_member" "workload_identity" {
  service_account_id = google_service_account.workload.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[${var.k8s_namespace}/${var.k8s_service_account}]"
}
