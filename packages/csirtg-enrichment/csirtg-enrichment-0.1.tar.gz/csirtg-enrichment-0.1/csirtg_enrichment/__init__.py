#!/usr/bin/env python3

import logging
import sys
import os
import textwrap
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from pprint import pprint
from multiprocessing import Pool

from csirtg_indicator import Indicator
from csirtg_indicator.constants import LOG_FORMAT
from csirtg_indicator.format import FORMATS

from csirtg_enrichment import plugins
from csirtg_enrichment.utils import load_plugins, get_argument_parser
from csirtg_enrichment.constants import RESOLVE_GEO, RESOLVE_FQDN, THREADS

logger = logging.getLogger(__name__)


def resolve(data):
    if isinstance(data, str):
        data = [data]

    p = load_plugins(plugins.__path__)

    data = \
        [Indicator(i, resolve_geo=RESOLVE_GEO, resolve_fqdn=RESOLVE_FQDN)
         for i in data]

    for pp in p:
        try:
            pp.process(data)

        except (KeyboardInterrupt, SystemExit):
            break

    pprint(data)
    return [i.__dict__() for i in data]


def main():  # pragma: no cover
    global THREADS
    p = get_argument_parser()
    p = ArgumentParser(
        description=textwrap.dedent('''\
        Env Variables:

        example usage:
            $ csirtg-enrichment 52.22.149.152,1.1.1.1,google.com,hotjasmine.su
        '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='csirtg-enrichment',
        parents=[p]
    )

    p.add_argument('indicators', help='Indicators to Enrich (CSV)')

    args = p.parse_args()

    loglevel = logging.getLevelName('INFO')

    if args.debug:
        loglevel = logging.DEBUG

    console = logging.StreamHandler()
    logging.getLogger('').setLevel(loglevel)
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger('').addHandler(console)

    if not sys.stdin.isatty():
        data = [l.rstrip("\n") for l in sys.stdin]
        if ',' in data[0]:
            data = data[0].split(',')
    else:
        data = args.indicators
        if ',' in data:
            data = data.split(',')
        else:
            data = [data]

    if len(data) < THREADS:
        THREADS = len(data)

    COLS = ['cc', 'asn', 'indicator']
    pool = Pool(THREADS)

    logger.info('enriching...')
    n = 0
    for output in pool.imap(resolve, data):
        logger.info('results for %s' % data[n])
        for l in FORMATS['table'](output, cols=COLS):
            print(l.rstrip("\n"))
        n += 1


if __name__ == "__main__":
    main()

