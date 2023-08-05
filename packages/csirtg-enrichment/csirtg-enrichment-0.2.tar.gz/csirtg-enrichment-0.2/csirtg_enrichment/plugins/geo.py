
import os
import logging
from pprint import pprint
import sys
from csirtg_geo import get as get_geo

from csirtg_indicator.utils.fqdn import resolve_fqdn, resolve_url
from csirtg_enrichment.constants import RESOLVE_GEO, RESOLVE_FQDN


logger = logging.getLogger(__name__)


def _resolve_indicator(i, itype):
    if itype == 'url':
        i = resolve_url(i)

    return resolve_fqdn(i)


def _valid(indicator):
    if not indicator.indicator:
        return False

    if indicator.itype not in ['ipv4', 'ipv6', 'fqdn', 'url']:
        return False

    if indicator.is_private:
        return False

    if indicator.cc and indicator.asn:
        return False

    return True


def _process(indicator):
    if not _valid(indicator):
        return indicator

    i = indicator.indicator
    if indicator.itype in ['fqdn', 'url']:
        if not RESOLVE_FQDN:
            return indicator
        
        i = _resolve_indicator(i, indicator.itype)

    try:
        geo = get_geo(i)

    except (TypeError, ValueError) as e:
        return indicator

    if not geo:
        return indicator

    for k, v in geo.items():
        setattr(indicator, k, v)

    return indicator


def process(data):
    if not RESOLVE_GEO:
        return

    if not isinstance(data, list):
        data = [data]

    for idx, i in enumerate(data):
        data[idx] = _process(i)


def main():
    # if you include this up top, it ruins the dep chain
    from csirtg_indicator import Indicator

    i = sys.argv[1]

    i = Indicator(i)
    process(i)

    pprint(i)


if __name__ == "__main__":
    main()
