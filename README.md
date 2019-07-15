# etherscan-exporter
Prometheus exporter for [etherscan.io](https://etherscan.io).

## Usage
```
docker run --rm -it -p 9308:9308 \
  -e LOGLEVEL=DEBUG \
  -e API_KEY="your_api_key" \
  -e ADDRESSES="0x90833394dB1b53f08B9D97dab8BEFf69FCf3bA49" \
  -e TOKENS='[{"contract":"0x9b70740e708a083c6ff38df52297020f5dfaa5ee","name":"Daneel","short":"DAN","decimals": 10},{"contract":"0xd26114cd6EE289AccF82350c8d8487fedB8A0C07","name":"OmiseGO","short":"OMG","decimals":18}]'
  --name etherscan-exporter \
  registry.gitlab.com/ix.ai/etherscan-exporter:latest
```

## Supported variables
* `API_KEY` (no default - **mandatory**) - set this to your Etherscan API key
* `URL` (default: https://api.etherscan.io/api) - set this to your Etherscan API secret
* `ADDRESSES` (no default) - a comma separated list of the ETH addresses to export
* `TOKENS` (no default) - a JSON object with the list of tokens to export (see below)
* `GELF_HOST` (no default) - if set, the exporter will also log to this [GELF](https://docs.graylog.org/en/3.0/pages/gelf.html) capable host on UDP
* `GELF_PORT` (defaults to `12201`) - the port to use for GELF logging
* `PORT` (defaults to `9308`) - the listen port for the exporter
* `LOGLEVEL` (defaults to `INFO`)

## Tokens
Example:
```
TOKENS='[{"contract":"0x9b70740e708a083c6ff38df52297020f5dfaa5ee","name":"Daneel","short":"DAN","decimals": 10}]'
```

The technical information can be found on [etherscan.io](https://etherscan.io/token/0x9b70740e708a083c6ff38df52297020f5dfaa5ee#readContract)
