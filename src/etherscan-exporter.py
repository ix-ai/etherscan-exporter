#!/usr/bin/env python3
"""Prometheus Exporter for Etherscan"""

import logging
import time
import os
import sys
import json
import requests
import pygelf
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, GaugeMetricFamily
from .lib import constants

LOG = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=os.environ.get("LOGLEVEL", "INFO"),
    format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

FILENAME = os.path.splitext(sys.modules['__main__'].__file__)[0]
version = f'{constants.VERSION}-{constants.BUILD}'


def configure_logging():
    """ Configures the logging """
    gelf_enabled = False

    if os.environ.get('GELF_HOST'):
        GELF = pygelf.GelfUdpHandler(
            host=os.environ.get('GELF_HOST'),
            port=int(os.environ.get('GELF_PORT', 12201)),
            debug=True,
            include_extra_fields=True,
            _ix_id=FILENAME
        )
        LOG.addHandler(GELF)
        gelf_enabled = True
    LOG.info('Initialized logging with GELF enabled: {}'.format(gelf_enabled))


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
        if not self.settings.get('api_key'):
            raise ValueError("Missing API_KEY environment variable.")

        if os.environ.get('TOKENS'):
            self.settings['tokens'] = (json.loads(os.environ.get("TOKENS")))

    def get_tokens(self):
        """ Gets the tokens from an account """

        time.sleep(1)  # Ensure that we don't get rate limited
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
                    LOG.exception('Exception caught: {}'.format(error))
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

    def get_balances(self):
        """ Gets the current balance for an account """
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
            LOG.exception('Exception caught: {}'.format(error))
            req = {}
        if req.get('message') == 'OK' and req.get('result'):
            for result in req.get('result'):
                self.accounts.update({
                    result['account']: float(result['balance'])/(1000000000000000000)
                })
        LOG.debug('Accounts: {}'.format(self.accounts))

    def describe(self):
        """ Just a needed method, so that collect() isn't called at startup """
        return []

    def collect(self):
        """The method that actually does the collecting"""
        metrics = {
            'account_balance': GaugeMetricFamily(
                'account_balance',
                'Account Balance',
                labels=['source_currency', 'currency', 'account', 'type']
            ),
        }
        self.get_balances()
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

        self.get_tokens()
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
    configure_logging()
    PORT = int(os.environ.get('PORT', 9308))
    LOG.info("Starting {} {} on port {}".format(FILENAME, version, PORT))
    REGISTRY.register(EtherscanCollector())
    start_http_server(PORT)
    while True:
        time.sleep(1)
