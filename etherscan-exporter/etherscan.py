#!/usr/bin/env python3
"""Prometheus Exporter for Etherscan"""

import logging
import time
import os
import json
import requests

log = logging.getLogger(__package__)


class Etherscan:
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
        log.info('Retrieving the tokens')
        for account in self.accounts:
            for token in self.settings['tokens']:
                log.debug(f"Retrieving the balance for {token['short']} on the account {account}")
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
                try:
                    req = requests.get(self.settings['url'], params=request_data).json()
                except (
                        requests.exceptions.ConnectionError,
                        requests.exceptions.ReadTimeout,
                ) as error:
                    log.exception(f'Exception caught: {error}')
                    req = {}
                if req.get('result') and int(req['result']) > 0:
                    self.tokens.update({
                        f"{account}-{token['short']}": {
                            'account': account,
                            'name': token['name'],
                            'name_short': token['short'],
                            'contract_address': token['contract'],
                            'value': int(req['result']) / (10**decimals) if decimals > 0 else int(req['result'])
                        }
                    })
                time.sleep(1)  # Ensure that we don't get rate limited
        log.debug(f'Tokens: {self.tokens}')
        return self.tokens

    def get_balances(self):
        """ Gets the current balance for an account """
        log.info('Retrieving the account balances')
        request_data = {
            'module': 'account',
            'action': 'balancemulti',
            'address': self.settings['addresses'],
            'tag': 'latest',
            'apikey': self.settings['api_key'],
        }
        try:
            req = requests.get(self.settings['url'], params=request_data).json()
        except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout,
        ) as error:
            log.exception(f'Exception caught: {error}')
            req = {}
        if req.get('message') == 'OK' and req.get('result'):
            for result in req.get('result'):
                self.accounts.update({
                    result['account']: float(result['balance'])/(1000000000000000000)
                })
        log.debug(f'Accounts: {self.accounts}')
        return self.accounts
