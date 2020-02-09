# etherscan-exporter

[![Pipeline Status](https://gitlab.com/ix.ai/etherscan-exporter/badges/master/pipeline.svg)](https://gitlab.com/ix.ai/etherscan-exporter/)
[![Docker Stars](https://img.shields.io/docker/stars/ixdotai/etherscan-exporter.svg)](https://hub.docker.com/r/ixdotai/etherscan-exporter/)
[![Docker Pulls](https://img.shields.io/docker/pulls/ixdotai/etherscan-exporter.svg)](https://hub.docker.com/r/ixdotai/etherscan-exporter/)
[![Gitlab Project](https://img.shields.io/badge/GitLab-Project-554488.svg)](https://gitlab.com/ix.ai/etherscan-exporter/)

Prometheus exporter for [etherscan.io](https://etherscan.io).

## Usage:
```
docker run --rm -it -p 9308:9308 \
  -e LOGLEVEL=DEBUG \
  -e API_KEY="your_api_key" \
  -e ADDRESSES="0x90833394dB1b53f08B9D97dab8BEFf69FCf3bA49" \
  -e TOKENS='[{"contract":"0x9b70740e708a083c6ff38df52297020f5dfaa5ee","name":"Daneel","short":"DAN","decimals": 10},{"contract":"0xd26114cd6EE289AccF82350c8d8487fedB8A0C07","name":"OmiseGO","short":"OMG","decimals":18}]'
  --name etherscan-exporter \
  ixdotai/etherscan-exporter:latest
```

## Supported variables:

| **Variable** | **Default**                    | **Mandatory** | **Description**  |
|:-------------|:------------------------------:|:-------------:|:-----------------|
| `API_KEY`    | -                              | **YES**       | set this to your Etherscan API key |
| `URL`        | `https://api.etherscan.io/api` | NO            | The URL of the Etherscan API |
| `ADDRESSES`  | -                              | NO            | A comma separated list of the ETH addresses to export |
| `TOKENS`     | -                              | NO            | A JSON object with the list of tokens to export (see [below](#tokens-variable)) |
| `LOGLEVEL`   | `INFO`                         | NO            | [Logging Level](https://docs.python.org/3/library/logging.html#levels) |
| `GELF_HOST`  | -                              | NO            | If set, the exporter will also log to this [GELF](https://docs.graylog.org/en/3.0/pages/gelf.html) capable host on UDP |
| `GELF_PORT`  | `12201`                        | NO            | Ignored, if `GELF_HOST` is unset. The UDP port for GELF logging |
| `PORT`       | `9308`                         | NO            | The port for prometheus metrics |

## Tokens variable:
Example:
```
TOKENS='[{"contract":"0x9b70740e708a083c6ff38df52297020f5dfaa5ee","name":"Daneel","short":"DAN","decimals": 10}]'
```

The technical information can be found on [etherscan.io](https://etherscan.io/token/0x9b70740e708a083c6ff38df52297020f5dfaa5ee#readContract)

## Tags and Arch

Starting with version v0.3.1, the images are multi-arch, with builds for amd64, arm64, armv7 and armv6.
* `vN.N.N` - for example v0.3.0
* `latest` - always pointing to the latest version
* `dev-master` - the last build on the master branch

## Resources:
* GitLab: https://gitlab.com/ix.ai/etherscan-exporter
* GitHub: https://github.com/ix-ai/etherscan-exporter
* Docker Hub: https://hub.docker.com/r/ixdotai/etherscan-exporter

See also [ix.ai/crypto-exporter](https://gitlab.com/ix.ai/crypto-exporter) for more usage examples, including Prometheus configuration
