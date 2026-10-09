# QobuzProxy image for the Home Assistant add-on.
# Built from the repository root by .github/workflows/ha-addon.yml:
#   docker build -f ha-addon/Dockerfile .

FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY qobuz_proxy/ ./qobuz_proxy/
COPY protos/ ./protos/

RUN pip install --no-cache-dir .

COPY ha-addon/run.sh /run.sh
RUN chmod +x /run.sh

# Home Assistant mounts the add-on's persistent storage at /data.
# config.yaml (speakers) and credentials.json (Qobuz login) live there.
ENV QOBUZPROXY_DATA_DIR=/data

ARG GIT_COMMIT=""
ENV QOBUZPROXY_COMMIT=$GIT_COMMIT

LABEL io.hass.type="addon"

CMD ["/run.sh"]
