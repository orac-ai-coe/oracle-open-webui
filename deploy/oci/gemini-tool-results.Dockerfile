# Overlay context: openai.py and oci.py from backend/open_webui.
ARG BASE_IMAGE
FROM ${BASE_IMAGE}
COPY openai.py /app/backend/open_webui/routers/openai.py
COPY oci.py /app/backend/open_webui/utils/oci.py
