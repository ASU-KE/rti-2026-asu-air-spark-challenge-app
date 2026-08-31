# Google observability runbook

The scaffold provides application instrumentation and namespaced collection declarations without enabling or changing any live Google Cloud or GKE setting.

## Signals implemented

### Logs and Error Reporting

Pino writes structured JSON to standard output. Each record carries `serviceContext`; active spans add Google trace/span correlation fields. Request and response bodies are never logged, known authorization/cookie and credential-like fields are redacted, and request/startup/shutdown errors are reduced to an allowlisted error type plus message-free stack frames. This preserves Error Reporting-compatible frame data without logging untrusted error messages or nested error objects.

Verify locally by calling a health endpoint and confirming one `request started` and one `request completed` record with request ID, method/status, and duration. Never add request/response bodies or credentials to logs.

### Traces

When `OTEL_ENABLED=true`, the API starts Node auto-instrumentation before loading Fastify and exports OTLP HTTP/protobuf to `OTEL_EXPORTER_OTLP_ENDPOINT`. The application does not authenticate directly to Google. An approved collector owns Google authentication and export to the Telemetry API.

The dev overlay intentionally contains fail-closed collector placeholders. The main trigger must provide the approved credential-free origin and matching namespace/workload selectors. Collector IAM, deployment, sampling, retention, and cost controls are separate Human-Gated prerequisites.

### Metrics

`/metrics` exposes bounded-label Prometheus data, including `rti_air_spark_http_request_duration_seconds` and process/runtime metrics. `PodMonitoring` selects only this app and scrapes named port `http` at `/metrics` every 30 seconds. A default-deny policy is paired with a scoped `gmp-system` rule and a same-namespace application rule; therefore every pod in `rti-air-spark-dev` can reach port 8080, including `/metrics`.

Before enabling deployment, confirm `rti-air-spark-dev` is a dedicated single-trust namespace. If other trust domains share it, replace the same-namespace rule with approved client labels or a separately restricted metrics boundary. Also verify the cluster has Managed Service for Prometheus and the `PodMonitoring` CRD, and ensure automatic application monitoring will not create a duplicate scraper.

## Dashboard and alert design gate

Dashboard widgets and alert policies are not fabricated in this scaffold. Generation requires the exact approved metric descriptor or PromQL/ListTimeSeries filter, units, thresholds, notification channels, and retention/evidence owner. Record those decisions in a ticket before creating dashboard or alert resources.

At minimum, the approved design should cover:

- request throughput and 5xx ratio;
- p50/p95/p99 request latency from the histogram;
- readiness/unavailable replicas, restart/crash-loop rate, and rollout failure;
- CPU throttling/utilization, memory working set/OOM, and HPA saturation;
- trace export failures and collector health;
- Error Reporting event rate;
- Cloud Build failure and rollback-failure notification.

No query, threshold, dashboard JSON/textproto, alert policy, or notification channel is included because none has been approved. This prevents silently selecting misleading metric math or creating billable/noisy monitoring state.

## Incident correlation

1. Start from the deployment/build ID and immutable image digest.
2. Inspect rollout status and Pod events using approved read-only access.
3. Correlate structured request errors to trace IDs.
4. Compare request latency/error signals with runtime CPU, memory, restarts, and HPA state.
5. If the candidate rollout is implicated, use the bounded digest rollback in [deployment rehearsal](deployment-rehearsal.md); do not use mutable tags or unbounded revision history.
6. Preserve redacted evidence according to [evidence and retrospective](../asdlc/evidence-and-retrospective.md).

Live dashboard, alert, collector, IAM, cluster-monitoring, and notification changes require a separate exact proposal and explicit human approval.
