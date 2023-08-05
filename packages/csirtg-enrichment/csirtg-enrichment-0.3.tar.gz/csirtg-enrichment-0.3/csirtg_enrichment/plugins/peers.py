
import os
from csirtg_indicator import Indicator
from csirtg_peers import get
from csirtg_enrichment.constants import RESOLVE_PEERS


def _process(indicator):

    if not indicator.is_ipv4:
        return indicator

    indicator.peers = []
    for p in get(indicator.indicator):
        indicator.peers.append(p)

    return indicator


def process(data):
    if not RESOLVE_PEERS:
        return

    if not isinstance(data, list):
        data = [data]

    for idx, i in enumerate(data):
        data[idx] = _process(i)


def main():
    i = Indicator('67.99.175.0')
    process(i)

    from pprint import pprint
    pprint(i)


if __name__ == '__main__':
    main()
