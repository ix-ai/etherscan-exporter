FROM alpine:latest
LABEL maintainer="docker@ix.ai" \
      ai.ix.repository="ix.ai/etherscan-exporter"

WORKDIR /app

COPY src/ /app

RUN apk --no-cache upgrade && \
    apk --no-cache add python3 py3-pip py3-requests py3-prometheus-client && \
    pip3 install --no-cache-dir -r requirements.txt

EXPOSE 9308

ENTRYPOINT ["python3", "/app/etherscan-exporter.py"]
