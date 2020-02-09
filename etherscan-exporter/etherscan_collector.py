#!/usr/bin/env python3
"""Prometheus Exporter for Etherscan"""

import logging
from prometheus_client.core import GaugeMetricFamily

log = logging.getLogger(__package__)


class EtherscanCollector:
    """ The EtherscanCollector class """

    accounts = {}
    tokens = {}

    def __init__(self, etherscan):
        self.etherscan = etherscan

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
        accounts = self.etherscan.get_balances()
        for account in accounts:
            metrics['account_balance'].add_metric(
                value=(accounts[account]),
                labels=[
                    'ETH',
                    'ETH',
                    account,
                    'etherscan'
                ]
            )

        tokens = self.etherscan.get_tokens()
        for token in tokens:
            metrics['account_balance'].add_metric(
                value=(tokens[token]['value']),
                labels=[
                    tokens[token]['name_short'],
                    tokens[token]['name_short'],
                    tokens[token]['account'],
                    'etherscan'
                ]
            )
        for metric in metrics.values():
            yield metric
