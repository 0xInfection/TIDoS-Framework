# TIDoS Framework -- Debian image
#
#   docker build -t tidos .
#   docker run -it --rm --env-file keys.env tidos        # console
#   docker run -it --rm tidos bash                        # drop to a shell
#
# The console runs as root (several modules open raw sockets); the container's
# default user is root, so nothing extra is needed. API keys come in through
# the environment -- see docs/setup.md.
FROM debian:bookworm-slim

LABEL org.opencontainers.image.title="TIDoS Framework" \
      org.opencontainers.image.description="The Offensive Web Application Penetration Testing Framework" \
      org.opencontainers.image.source="https://github.com/0xInfection/TIDoS-Framework" \
      org.opencontainers.image.licenses="GPL-3.0"

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH

# System packages the modules shell out to or build against.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 python3-venv python3-dev \
        build-essential pkg-config \
        libxml2 libexiv2-dev default-libmysqlclient-dev \
        nmap tcpdump dnsutils traceroute iputils-ping tor \
        git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/TIDoS

# Install Python dependencies first so the layer caches across code changes.
COPY requirements.txt ./
RUN python3 -m venv "$VIRTUAL_ENV" \
    && pip install --no-cache-dir -r requirements.txt

# The framework itself.
COPY . .

# `tidos` launcher: start the console from the repo root (it reads core/doc/*
# and writes tmp/logs/ relative to the working directory).
RUN printf '#!/bin/sh\ncd /opt/TIDoS && exec python3 -B tidconsole.py "$@"\n' \
        > /usr/local/bin/tidos \
    && chmod +x /usr/local/bin/tidos

# Default to the console; `docker run ... tidos bash` drops to a shell instead.
CMD ["tidos"]
