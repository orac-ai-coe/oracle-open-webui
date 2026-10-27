# Remote code synchronization — 27 October 2026

The running `open-webui` deployment on `openwebui` was copied into this checkout
and verified by SHA-256. All 5,963 exported application files and 53 exported
host deployment files match the remote snapshot. There were no checksum mismatches.

| Remote files | Local destination |
| --- | --- |
| `/app/backend/` source and static assets | `backend/` |
| `/app/build/` compiled frontend, including current branding hooks | `build/` |
| `/app/build/static/` build-source static assets | `static/static/` |
| `/app/package.json`, `/app/CHANGELOG.md` | Existing matching root files |
| `/opt/openwebui-branding/` deployment code and assets | `deploy/oci/remote-host/openwebui-branding/` |
| `/opt/openwebui-patches/` OCI patch code and tests | `deploy/oci/remote-host/openwebui-patches/` |
| `/opt/open-webui/start.sh` active launch helper | `deploy/oci/remote-host/open-webui/start.sh` |

The backend source already matched the server, including the OCI schema and
GPT-6 Luna compatibility patches. This synchronization copied two changed backend
static files, four added backend branding/font files, the 5,646-file compiled
frontend, and 53 deployment files. The frontend source assets already matched
all 21 files in the deployed static-source directory.

The server contains compiled frontend files rather than the Svelte source tree.
Existing local Svelte, title, and branding source edits were preserved. `build/`
is generated output and remains Git-ignored; it is nevertheless present on disk.
The host deployment directories are snapshots of server scripts, including
historical patch revisions. They reference server-specific paths and existing
local image tags; the root project Dockerfile remains the normal full-source
build entry point.

Original local files that were replaced are saved under
`.deployment/remote-sync-20261027/local-before/`. Its parent synchronization
directory contains the pre-sync tracked diff, downloaded archives, full remote
hash manifests, copied-file list and `sync-report.json`. No local-only files were deleted. User data,
databases, runtime credentials, container environment snapshots, runtime caches,
Python bytecode and AppleDouble metadata were excluded.
