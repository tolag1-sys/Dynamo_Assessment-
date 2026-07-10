# Base image must be an approved base, pinned by @sha256 digest.
# Replace the digest below with the one from your project's approved-base list.
# Resolve it with:  docker inspect --format='{{index .RepoDigests 0}}' <approved:tag>
FROM python:3.13-slim-bookworm@sha256:REPLACE_WITH_APPROVED_DIGEST

RUN pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5

WORKDIR /app

COPY access.log /app/access.log
