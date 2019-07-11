#!/usr/bin/env python3
"""Prometheus Exporter for Etherscan"""

import logging
import time
import os
import sys
import json
import requests
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, GaugeMetricFamily

LOG = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=os.environ.get("LOGLEVEL", "INFO"),
    format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class EtherscanCollector:
    """ The EtherscanCollector class """

    accounts = {}
    tokens = {}

    def __init__(self):
        self.settings = {
            'api_key': os.environ.get("API_KEY"),
            'url': os.environ.get("URL", 'https://api.etherscan.io/api'),
            'addresses': os.environ.get("ADDRESSES"),
            'tokens': [],
        }
        if os.environ.get('TOKENS'):
            self.settings['tokens'] = (json.loads(os.environ.get("TOKENS")))

    def _get_tokens(self):
        # Ensure that we don't get blocked
        time.sleep(1)
        for account in self.accounts:
            for token in self.settings['tokens']:
                request_data = {
                    'module': 'account',
                    'action': 'tokenbalance',
                    'contractaddress': token['contract'],
                    'address': account,
                    'tag': 'latest',
                    'apikey': self.settings['api_key'],
                }
                decimals = 18
                if token.get('decimals', -1) >= 0:
                    decimals = int(token['decimals'])
                LOG.debug('{} decimals for {}'.format(decimals, token['short']))
                try:
                    req = requests.get(self.settings['url'], params=request_data).json()
                except (
                        requests.exceptions.ConnectionError,
                        requests.exceptions.ReadTimeout,
                ) as error:
                    LOG.warning(error)
                    req = {}
                if req.get('result') and int(req['result']) > 0:
                    self.tokens.update({
                        '{}-{}'.format(account, token['short']): {
                            'account': account,
                            'name': token['name'],
                            'name_short': token['short'],
                            'contract_address': token['contract'],
                            'value': int(req['result']) / (10**decimals) if decimals > 0 else int(req['result'])
                        }
                    })

        LOG.debug('Tokens: {}'.format(self.tokens))

    def _get_balances(self):
        request_data = {
            'module': 'account',
            'action': 'balancemulti',
            'address': self.settings['addresses'],
            'tag': 'latest',
            'apikey': self.settings['api_key'],
        }
        LOG.debug('Request data: {}'.format(request_data))
        try:
            req = requests.get(self.settings['url'], params=request_data).json()
        except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout,
        ) as error:
            LOG.warning(error)
            req = {}
        if req.get('message') == 'OK' and req.get('result'):
            for result in req.get('result'):
                self.accounts.update({
                    result['account']: float(result['balance'])/(1000000000000000000)
                })
        LOG.debug('Accounts: {}'.format(self.accounts))

    def collect(self):
        """The method that actually does the collecting"""
        metrics = {
            'account_balance': GaugeMetricFamily(
                'account_balance',
                'Account Balance',
                labels=['source_currency', 'currency', 'account', 'type']
            ),
        }
        self._get_balances()
        for account in self.accounts:
            metrics['account_balance'].add_metric(
                value=(self.accounts[account]),
                labels=[
                    'ETH',
                    'ETH',
                    account,
                    'etherscan'
                ]
            )

        self._get_tokens()
        for token in self.tokens:
            metrics['account_balance'].add_metric(
                value=(self.tokens[token]['value']),
                labels=[
                    self.tokens[token]['name_short'],
                    self.tokens[token]['name_short'],
                    self.tokens[token]['account'],
                    'etherscan'
                ]
            )
        for metric in metrics.values():
            yield metric


if __name__ == '__main__':
    LOG.info("Starting")
    REGISTRY.register(EtherscanCollector())
    start_http_server(9308)
    while True:
        time.sleep(1)
