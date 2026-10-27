# Overlay for an existing deployment image. The context supplies the live env.py
# (with the name change) and openai.py so prior OCI patches are retained.
ARG BASE_IMAGE
FROM ${BASE_IMAGE}
COPY env.py /app/backend/open_webui/env.py
COPY openai.py /app/backend/open_webui/routers/openai.py
COPY assets/ /app/build/static/
COPY index.html /app/build/index.html
ENV WEBUI_NAME="Oracle - OpenWebUI"
