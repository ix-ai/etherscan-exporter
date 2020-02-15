#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" initializes etherscan-exporter """

import os
from .lib import log as logging
from .lib import constants

log = logging.setup_logger(
    name=__package__,
    level=os.environ.get('LOGLEVEL', 'INFO'),
    gelf_host=os.environ.get('GELF_HOST'),
    gelf_port=int(os.environ.get('GELF_PORT', 12201)),
    _ix_id=__package__,
    _version=f'{constants.VERSION}-{constants.BUILD}',
)
