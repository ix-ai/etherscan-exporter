FROM alpine:latest
LABEL maintainer="docker@ix.ai" \
      ai.ix.repository="ix.ai/etherscan-exporter"

COPY etherscan-exporter/requirements.txt /etherscan-exporter/requirements.txt

RUN apk --no-cache upgrade && \
    apk --no-cache add python3 py3-pip py3-requests py3-prometheus-client && \
    pip3 install --no-cache-dir -r /etherscan-exporter/requirements.txt

COPY etherscan-exporter/ /etherscan-exporter/
COPY etherscan-exporter.sh /usr/local/bin/etherscan-exporter.sh

EXPOSE 9308

ENTRYPOINT ["/usr/local/bin/etherscan-exporter.sh"]
