# Demo artifact and offline contingency

This runbook protects the Event Critical Path when Cloud Build, Artifact Registry, GKE, the network, or the live demo environment is unavailable. It does not authorize a cloud build, registry push, cluster access, or deployment.

## Prepare before the event

From the exact reviewed commit, on a workstation with a functioning Docker daemon:

1. Run `npm ci`, `npm run validate`, and `npm run validate:delivery`.
2. Build `rti-air-spark-demo:<full-commit-sha>` from the repository `Dockerfile`.
3. Run `scripts/ci/smoke-container.sh rti-air-spark-demo:<full-commit-sha>`.
4. Record the commit SHA and `docker image inspect --format '{{.Id}}' rti-air-spark-demo:<full-commit-sha>` output in a text manifest.
5. Export the image with `docker save --output rti-air-spark-demo-<full-commit-sha>.tar rti-air-spark-demo:<full-commit-sha>`.
6. Create a checksum with `shasum -a 256 rti-air-spark-demo-<full-commit-sha>.tar > rti-air-spark-demo-<full-commit-sha>.tar.sha256`.
7. Copy the tar archive, checksum, and text manifest to the approved encrypted team storage and to the designated demo workstation. Do not store credentials, `.env` files, user data, prompts, or model responses in the artifact.

The accountable human records the artifact location and verification result in ticket/session evidence. Regenerate the artifact after any accepted application change; never relabel an older image as a newer commit.

## Rehearse the offline path

On the designated demo workstation:

1. Verify the archive with `shasum -a 256 --check rti-air-spark-demo-<full-commit-sha>.tar.sha256`.
2. Load it with `docker load --input rti-air-spark-demo-<full-commit-sha>.tar`.
3. Confirm the loaded image ID matches the text manifest.
4. Run the standard container smoke script.
5. Start the image bound only to localhost with the same read-only filesystem, bounded `/tmp`, dropped capabilities, and no-new-privileges controls used by the smoke script.
6. Verify `/health/live`, `/health/ready`, `/api/v1/status`, `/openapi.json`, `/metrics`, and `/` before rehearsing the demo.
7. Disconnect the network and repeat the planned demonstration. Record which future product capabilities are unavailable offline and prepare a truthful narrated fallback or approved prerecorded evidence for them.

## Event decision rule

- Use the reviewed GKE deployment when rollout and smoke evidence is current.
- Use the checksum-verified offline image when cloud or venue reliability threatens the demo.
- Do not improvise a privileged manual deployment, bypass Cloud Build controls, expose an unreviewed public endpoint, or add credentials during the event.
- If neither path verifies, present the validated design and recorded evidence without claiming a working live deployment.
