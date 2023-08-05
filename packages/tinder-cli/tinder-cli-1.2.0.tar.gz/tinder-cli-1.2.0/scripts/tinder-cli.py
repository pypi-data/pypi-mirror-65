#!/usr/bin/env python3

import argparse
import getpass
import re
import os
import os.path
import sys

import requests

from tinder_cli import cli


def main():
    args = parse_args()
    file_path = os.path.expanduser('~') + '/.tinder-cli'

    if not os.path.isfile(file_path):
        tinder_token = input('tinder token: ')

        with open(file_path, 'w') as f:
            f.write(tinder_token)

    with open(file_path, 'r') as f:
        tinder_token = f.read().strip()

    requests.urllib3.disable_warnings()
    session = cli.client.get_session(tinder_token)

    try:
        result = getattr(cli, 'cmd_{}'.format(args.cmd))(
            session, tinder_id=args.id
        )

    except requests.exceptions.HTTPError as e:
        result = 'error occured - {}'.format(str(e))
        os.remove(file_path)

    print(result)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=cli.COMMANDS,
                        metavar='COMMAND', help=', '.join(cli.COMMANDS))
    parser.add_argument('--id', action='store', type=str, default=False,
                        metavar='TINDER ID', help='tinder profile ID')

    return parser.parse_args()


if __name__ == "__main__":
    main()
