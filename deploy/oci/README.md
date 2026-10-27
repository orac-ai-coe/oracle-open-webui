# Exported OCI OpenWebUI configuration

This profile was pulled from the running `open-webui` container on `openwebui`
(`https://orac-ai.com`) on 26 October 2026. The production VM was not modified.

## Files

- `runtime.json`: 22 application settings, the OpenWebUI `OCI-GenAI-Users` group,
  and 43 model definitions with group-level access rules. Includes the OCI
  endpoint, its 42 explicitly configured models, automatic `User` role, disabled
  password signup, and the default application group.
- `.env.example`: non-secret template for the container environment, including
  the existing OCI identity-domain OIDC client and callback configuration.
- `compose.yaml`: builds this checkout into a separate local container and volume.
- `apply.py`: validates the profile or imports its settings and access definitions
  using the target image's application models. It maps groups by name rather
  than reusing production database IDs. Existing group memberships are untouched.

The ignored `.deployment/` directory at the repository root contains the actual
exported credentials in `openwebui.env`, a full configuration-table snapshot in
`runtime.private.json`, and the model/group export in `model-access.private.json`.
These files have mode `0600`; the directory is excluded from Git and Docker build
contexts. The environment file uses Compose `format: raw` so credentials and
JSON values are not interpolated. A separate local session-signing key was
generated; the production session-signing key was not copied.

No users, passwords, session tokens, chats, uploaded documents, or group
memberships were copied. Individual-user model grants are excluded. The local
checkout's application code and the existing root Compose file are unchanged.

## Use with this checkout

1. Review `.deployment/openwebui.env`. It currently retains the production
   `WEBUI_URL` and `OPENID_REDIRECT_URI`. To use SSO on another address, register
   that exact callback in the OCI confidential application and update both
   environment variables. Update `webui.url` in `runtime.json` to the same site
   before applying the profile. Credentials in the private file access the real
   OCI services; substitute separate credentials when needed.
2. Build and start the separate local deployment from the repository root:

   ```sh
   docker compose -f deploy/oci/compose.yaml up -d --build
   ```

   Use `docker-compose` instead of `docker compose` if Compose is installed as a
   standalone command. The service binds to `127.0.0.1:3000` and uses its own
   persistent volume; it does not reuse the production volume.
3. Open `http://localhost:3000` and create the first local administrator account.
4. Validate and then import the settings, default group and model access:

   ```sh
   python3 deploy/oci/apply.py
   python3 deploy/oci/apply.py --apply
   ```

   The importer backs up the target settings inside its data volume before
   writing, creates missing groups, and creates or updates the exported model
   IDs. Existing accounts and memberships are not imported. Run it only against
   the intended local container; `--container` overrides `open-webui-local`.

For a new checkout, copy `deploy/oci/.env.example` to
`.deployment/openwebui.env` and supply the credentials before starting Compose.

## OCI IAM configuration is separate

Corporate Production SAML federation, first-login user provisioning, the OCI IAM
`OCI-GenAI-Users` group and application grants are managed in the `aistudio`
identity domain. They were not changed or recreated by this local export.
The OpenWebUI group with the same name is a separate application group.

## Validation performed

The saved profile and Compose configuration are validated locally. No local image
was built or started, and no new end-to-end SSO or model-inference test was run as
part of this export.

## Live model retirement cleanup — 27 October 2026

The live Frankfurt OCI endpoint explicitly reported eight configured model IDs as
retired: GPT-4.1 Nano, o1, o3 Mini and o4 Mini, each with its undated and dated
version. Those IDs were removed from the production connection, model definitions
and corresponding model access grants. The saved public and private profiles were
updated to match, so importing them will not restore the retired entries.

All 42 retained connection IDs returned HTTP 200 and a short text completion in
direct inference checks from the deployed container. GPT-5/6 and o3 checks used
max_completion_tokens; other models used max_tokens. This verifies simple text
inference, not every feature or user-specific chat configuration.

A mode-0600 database backup was created on the server before the change:
/app/backend/data/backups/model-retirement-20261027T125251Z.sqlite3.

The OpenWebUI model-list API returned only the retained models plus the existing
GPT-OSS alias. Non-streaming chat through the application's main chat endpoint
returned HTTP 200 and text replies for GPT-OSS 120B and GPT-5 Mini.

Standard-user streaming chat also returned HTTP 200 and text replies for Gemini
2.5 Flash and GPT-5 Mini. No restart was needed; the running application read the
updated configuration and model records immediately.

## GPT-6 Luna function-tool compatibility — 27 October 2026

The OCI Chat Completions endpoint rejects GPT-6 Luna function tools when reasoning
is enabled. Simple text inference does not expose this restriction. The deployed
OpenWebUI router now sets reasoning_effort to none only when sending function
tools to openai.gpt-6-luna through an OCI Generative AI Chat Completions connection.
This applies after model and chat parameters are combined, so saved chat settings
cannot reintroduce the incompatible combination. Requests without function tools,
other models, other providers and Responses connections keep their settings.

The patch is in backend/open_webui/routers/openai.py in this checkout and was
applied to the running container, followed by an application restart. A container
recreation must include this source change in the rebuilt image. The prior router
is backed up on the server at:
/app/backend/data/backups/openai-router-before-luna-tools-20261027T130155Z.py.

Live checks after deployment passed for a standard user: a function call with
reasoning_effort=low, a streamed function call with reasoning_effort=high, a
tool-result continuation, and reasoning-only chat without tools. All returned
HTTP 200. One initial continuation probe returned an upstream HTTP 502; the
subsequent probe with an explicit assistant content=null returned a text reply.

## Oracle theme and co-branding — 27 October 2026

The live deployment at `https://orac-ai.com` now uses the application name
`Oracle - OpenWebUI`. The frontend fallback title and backend default match;
names already containing `OpenWebUI` do not gain a duplicate attribution suffix.

`static/static/custom.css` is the browser-ready adaptation of `style-ref.css`.
It expands the reference's Tailwind directives and maps its dark background
(`#0D1117`), card (`#1B1F2E`), border (`#30363D`), Inter font and Oracle red
(`#C74634`) onto OpenWebUI. `static/static/loader.js` replaces the existing
sidebar and sign-in logo with `static/static/oracle-openwebui.svg`, combining the
supplied Oracle O, a pipe, and the original OpenWebUI Oi logo. There is no added
top bar or reserved header space. Existing logo links and sidebar controls keep
their behavior; the combined mark scales down in the collapsed sidebar.
The loader defaults each browser to dark mode once; subsequent user theme choices
remain available. The supplied image is saved unchanged as
`static/static/oracle-o.png`; the combined SVG embeds the original raster assets.

The deployed image is `oracle-openwebui:sidebar-branding-20261027`. It derives
from `oracle-openwebui:branding-20261027` (`108c6c8c10d1`), which derives from the
existing OCI schema-patched image and carries
forward the live GPT-6 Luna router patch. No frontend bundle or application
version upgrade was required: the application already loads the static
`custom.css` and `loader.js` hooks. `branding.Dockerfile` records the overlay
layout; its build context supplies the patched live `env.py`, `openai.py`,
`index.html`, and the branding files under `assets/`. Normal full source builds use
the updated source files directly.

The server's `/opt/open-webui/start.sh` and private `webui.env` now reference the
branded image and exact name. The original container is retained, stopped with
restart disabled, as `open-webui-before-sidebar-branding-20261027`. The earlier original backup
`open-webui-before-branding-20261027` also remains stopped. Private deployment
and rollback files for the latest revision are in
`/opt/openwebui-branding/sidebar-20261027/` (mode 0700),
including the prior container inspection and startup/environment files. To roll
back, stop the current container, rename it, rename the retained container to
`open-webui`, restore its `unless-stopped` restart policy, and start it; also
restore the saved startup/environment files. The persistent application data
volume is shared by the successive containers and must only have one running
application container at a time.

Validation: public health, configuration, manifest and branding assets
returned HTTP 200. The configuration and manifest report the exact requested
name. Browser review of the initial revision verified the sign-in title and palette.
The revised layout removes the top bar and places the combined mark in the
existing logo position. The SSO
button reached the existing OCI identity-domain sign-in page. A container restart
preserved the theme assets and name; hashes confirmed both previous OCI source
patches were retained. An authenticated chat UI and a new complete SSO login were
not exercised during this appearance change.

Latest revision verification: the deployed container is healthy, public branding
assets match the local SHA-256 hashes, and the sign-in page shows the combined
Oracle O | Oi mark at the original top-left logo position with no top bar or
header offset. Authenticated sidebar selectors were checked against the source;
an authenticated browser session was not available for visual review.

Equal-size logo revision: both logo tiles occupy 32 × 32 SVG units. The Oi
asset’s transparent outer padding is excluded by its SVG viewBox, so its visible
tile matches the Oracle tile. Live static source and served files were updated
without a restart. The recreation helper now uses the derived image
`oracle-openwebui:equal-logos-20261027`; rollback files are in
`/opt/openwebui-branding/equal-logos-20261027/`.

Login heading revision: the sign-in card now displays the combined equal-size
Oracle O | Oi logos instead of the visible “Sign in to Oracle - OpenWebUI”
heading. The original text remains available to screen readers. The separate
corner logo is hidden on this sign-in view, while the sidebar branding remains.
The live static files and recreation image `oracle-openwebui:login-heading-20261027`
include the change; rollback files are in
`/opt/openwebui-branding/login-heading-20261027/`.

Sidebar caption revision: `Oracle-OpenWebUI` is centered below the combined
logos. It uses locally served Oracle Sans Regular at `calc(12px - 2pt)`
(7pt / 9.333px), two points smaller than the previous 12px caption. The grid
keeps the sidebar collapse control to the right. An isolated sidebar layout
preview verified that the caption starts below the logos and that Oracle Sans
is loaded; the authenticated live sidebar was not available for visual review.
The public font, script and stylesheet returned HTTP 200 and matched local
assets. The recreation image is `oracle-openwebui:sidebar-caption-20261027`, with
rollback files in `/opt/openwebui-branding/sidebar-caption-20261027/`.

Sidebar caption size update: the caption now uses Oracle Sans at 16px with a
20px line height, retaining its position below the logos. The live static source
and served CSS match the recreation image
`oracle-openwebui:sidebar-caption16-20261027`; rollback files are under
`/opt/openwebui-branding/sidebar-caption16-20261027/`.

Chat welcome logo revision: the model icon above the empty-chat composer now
uses the supplied Oracle O image. The static loader targets only the welcome
area; the source component `Placeholder.svelte` also references the Oracle asset
for future full frontend builds. The deployed static overlay and recreation
image `oracle-openwebui:chat-oracle-logo-20261027` include the change. Rollback
files are under `/opt/openwebui-branding/chat-oracle-logo-20261027/`. Public
asset/health checks passed; an authenticated live chat UI was not available for
visual review.

Assistant avatar revision: icons beside assistant responses now use the Oracle O
asset. The runtime hook targets `img.assistant-message-profile-image`, and the
source `ResponseMessage.svelte` uses the same Oracle image for future builds.
The live overlay and recreation image
`oracle-openwebui:assistant-oracle-logo-20261027` include this change; rollback
files are in `/opt/openwebui-branding/assistant-oracle-logo-20261027/`. Public
script, Oracle image and health checks passed. No authenticated live browser
review was performed for this revision.

## Full remote code synchronization — 27 October 2026

The running application code, compiled frontend and host-side deployment code
have been pulled into this checkout and verified by checksum. See
[REMOTE_SYNC.md](REMOTE_SYNC.md) for destinations, counts and backup locations.
