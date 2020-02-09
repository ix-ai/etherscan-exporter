#!/usr/bin/env python3
"""Prometheus Exporter for Etherscan"""

import logging
import time
import os
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY
from .lib import constants
from .etherscan_collector import EtherscanCollector
from .etherscan import Etherscan


log = logging.getLogger(__package__)
version = f'{constants.VERSION}-{constants.BUILD}'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9308))
    log.warning(f'Starting {__package__} {version} on port {port}')
    log.warning("The label 'source_currency' is deprecated and will likely be removed soon")

    etherscan = Etherscan()
    REGISTRY.register(EtherscanCollector(etherscan))
    start_http_server(port)
    while True:
        time.sleep(1)
