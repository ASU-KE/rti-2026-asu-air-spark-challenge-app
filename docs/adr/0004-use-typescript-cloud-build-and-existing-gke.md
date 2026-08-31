---
status: accepted
---

# Use TypeScript, Cloud Build, and the existing GKE development cluster

The Challenge Application will use a TypeScript web/API workspace, vendor and adapt the `ASU-KE/rti-template-gcp-app` contents, and deploy through Cloud Build to `websvcs-gke-private-dev` in `asu-ke-rto-web-svcs/us-west4`. A least-privilege pull-request trigger will run the authoritative install, lint, typecheck, test, scan, container-build, smoke-test, and manifest-validation pipeline without deployment access; a separate `main` trigger will repeat those controls for the merged commit, push an immutable image, deploy it to `rti-air-spark-dev`, verify rollout and smoke tests, and roll back failures. The application will integrate OpenTelemetry with Google Cloud Logging, Monitoring, Managed Service for Prometheus, Trace, and Error Reporting so delivery and runtime behavior are observable during the pilot.
