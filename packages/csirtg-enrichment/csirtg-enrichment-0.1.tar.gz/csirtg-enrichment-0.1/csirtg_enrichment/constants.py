import os
from multiprocessing import cpu_count
from ._version import get_versions
VERSION = get_versions()['version']
del get_versions

RESOLVE_GEO = True
if os.getenv('CSIRTG_ENRICHMENT_GEO', '1') == '0':
    RESOLVE_GEO = False

RESOLVE_FQDN = True
if os.getenv('CSIRTG_ENRICHMENT_FQDN', '1') == '0':
    RESOLVE_FQDN = False

RESOLVE_PEERS = True
if os.getenv('CSIRTG_ENRICHMENT_PEERS', '1') == '0':
    RESOLVE_PEERS = False

THREADS = os.getenv('THREADS', cpu_count() * 1.5)
THREADS = int(THREADS)
