FROM registry.gitlab.com/ix.ai/alpine:latest
LABEL MAINTAINER="docker@ix.ai"

ARG PORT

RUN apk add --no-cache py3-requests

ENV LOGLEVEL=INFO PORT=${PORT}

COPY src/etherscan-exporter.py /

EXPOSE ${PORT}

ENTRYPOINT ["python3", "/etherscan-exporter.py"]
