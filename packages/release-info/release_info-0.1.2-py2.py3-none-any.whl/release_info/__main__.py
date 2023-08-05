# coding: utf-8

import sys

from .__init__ import __version__
from .release_info import release_info
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='programmatically extractable python release information'
    )
    parser.add_argument(
        '--config',
        help=f'path to alternative config file (default: {release_info.config_path})',
    )
    parser.add_argument(
        '--type', help=f'compiler type to work on: [cpython, tbd] (default: cpython)'
    )
    parser.add_argument('--version', action='version', version=__version__)
    subparsers = parser.add_subparsers()
    sp = []
    sp.append(subparsers.add_parser('update', help='download release_info.pon to config dir'))
    sp[-1].set_defaults(func=release_info.download_data)
    sp.append(
        subparsers.add_parser(
            'check', help='check release_info.pon and optionally add/overwrite info'
        )
    )
    sp[-1].set_defaults(func=release_info.check)
    sp.append(
        subparsers.add_parser('current', help='list of current major.minor.micro versions')
    )
    sp[-1].add_argument(
        '--dd', help=f'show releases current on date dd (YYYY-MM-DD), default: today'
    )
    sp[-1].set_defaults(func=release_info.print_current)
    sp.append(subparsers.add_parser('pre', help='list of not yet finalized releases'))
    sp[-1].add_argument(
        '--dd', help=f'show releases current on date dd (YYYY-MM-DD), default: today'
    )
    sp[-1].set_defaults(func=release_info.print_pre)
    sp.append(subparsers.add_parser('download', help='download/extract a particular version'))
    sp[-1].add_argument('--dir', help=f'directory where source tar is downloaded to')
    sp[-1].add_argument('--extract', action='store_true', help=f'extract downloaded tar file')
    sp[-1].add_argument(
        '--force',
        action='store_true',
        help=f'force download (and extraction), normally skipped if there',
    )
    sp[-1].add_argument('version', help=f'version major.minor.micor to download')
    sp[-1].set_defaults(func=release_info.download)
    args = parser.parse_args()
    if args.config:
        release_info.config_path = args.config
    try:
        f = args.func
    except AttributeError:
        parser.parse_args(['-h'])
    res = f(args=args)
    sys.exit(0 if res is None else res)


if __name__ == '__main__':
    main()
