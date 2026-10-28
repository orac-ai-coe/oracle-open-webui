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

## Refresh — 28 October 2026

The running container was exported again and compared with this checkout.
All 5,964 application files already matched, including the Gemini tool-result
normalizer and router change. All 21 deployed static-source assets also matched.

The host deployment export contained 56 files. Three missing files from
`openwebui-patches/gemini-tool-results-20261027/` were copied into
`deploy/oci/remote-host/`: `Dockerfile`, `oci.py`, and `openai.py`. The changed
historical branding file `openwebui-branding/20261027/index.html` was also copied.
Its previous local version is preserved under
`.deployment/remote-sync-20261028/local-before/`.

All application and host deployment files passed SHA-256 verification after
the refresh. Archives, manifests, the pre-sync local diff, copied-file list and
`sync-report.json` are in `.deployment/remote-sync-20261028/`. Local-only files
were retained, and the same private-data and runtime-cache exclusions apply.
The remote container was not modified during this refresh.
