#!/bin/bash
set -euo pipefail
install -d -m 700 /opt/open-webui
if [ ! -f /opt/open-webui/webui.env ]; then
  umask 077
  printf 'WEBUI_SECRET_KEY=%s\nWEBUI_AUTH=True\n' "$(openssl rand -hex 32)" > /opt/open-webui/webui.env
fi
docker image inspect oracle-openwebui:gemini-tool-results-20261027 >/dev/null
docker volume create open-webui
docker run -d --name open-webui --restart unless-stopped \
  -p 127.0.0.1:3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  --env-file /opt/open-webui/webui.env \
  -v open-webui:/app/backend/data \
  oracle-openwebui:gemini-tool-results-20261027
