"""
Example usage of daikinapi module

use e.g. with "python example.py 192.168.1.3"
"""
import argparse
import logging

from daikinapi import Daikin

PARSER = argparse.ArgumentParser(
    description="Get metrics from Daikin airconditioning wifi module"
)
PARSER.add_argument(
    "-v", "--verbose", help="set logging to debug", action="store_true", default=False,
)
PARSER.add_argument("hosts", help="list of airconditioning units to query", nargs="*")
ARGS = PARSER.parse_args()

LOGFORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

if ARGS.verbose:
    logging.basicConfig(level=logging.DEBUG, format=LOGFORMAT)
else:
    logging.basicConfig(level=logging.INFO, format=LOGFORMAT)
    logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(
        logging.WARNING
    )

logging.debug("starting with arguments: %s", ARGS)

for host in ARGS.hosts:
    API = Daikin(host)
    print(API)
    for attribute in API.ATTRIBUTES:
        print(attribute, getattr(API, attribute))
