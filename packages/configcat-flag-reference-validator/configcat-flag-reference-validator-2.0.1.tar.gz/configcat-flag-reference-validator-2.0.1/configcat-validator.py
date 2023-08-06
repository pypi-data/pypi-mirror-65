#!/usr/bin/env python

import argparse
import logging
import sys

from configcat.reference_validator.config_fetcher import ConfigFetcher
from configcat.reference_validator.reference_finder import ReferenceFinder
from configcat.reference_validator.reference_validator import ReferenceValidator

log = logging.getLogger(sys.modules[__name__].__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("configcat_sdk_key",
                        help="The SDK Key of your ConfigCat project.")
    parser.add_argument("search_dir",
                        help="The directory to scan for flag references.")
    parser.add_argument("-s", "--configcat_cdn_server",
                        help="The domain name of the ConfigCat CDN where you ConfigCat configuration file is stored.",
                        default="cdn.configcat.com")
    parser.add_argument("-f", "--fail_on_warnings",
                        help="Signals a build error when the validation fails. By default only warnings are showed.",
                        default=False,
                        const=True,
                        nargs='?',
                        type=str2bool)
    parser.add_argument("-v", "--verbose",
                        default=False,
                        const=True,
                        nargs='?',
                        help="Turns on detailed logging.",
                        type=str2bool)

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    fetcher = ConfigFetcher(args.configcat_sdk_key, args.configcat_cdn_server)
    finder = ReferenceFinder(args.search_dir)

    remote_keys = fetcher.get_flag_keys()

    validation_result = ReferenceValidator.validate(set(remote_keys), finder.find_references(remote_keys))

    if not validation_result and args.fail_on_warnings:
        sys.exit(1)

    if validation_result:
        log.info("PASSED. Everything's fine, didn't find any unused feature flags.")


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':
    main()
