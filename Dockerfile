FROM alpine:latest
LABEL maintainer="docker@ix.ai"

ARG PORT=9308
ARG LOGLEVEL=INFO

RUN apk --no-cache upgrade && \
    apk add --no-cache py3-requests && \
    pip3 install --no-cache-dir prometheus_client pygelf

ENV LOGLEVEL=${LOGLEVEL} PORT=${PORT}

COPY src/etherscan-exporter.py /

EXPOSE ${PORT}

ENTRYPOINT ["python3", "/etherscan-exporter.py"]
