FROM hub.ix.ai/docker/alpine:latest
LABEL ai.ix.maintainer="docker@ix.ai"

RUN apk add --no-cache py3-requests

ENV LOGLEVEL=INFO

COPY src/etherscan-exporter.py /

EXPOSE 9308

ENTRYPOINT ["python3", "/etherscan-exporter.py"]
