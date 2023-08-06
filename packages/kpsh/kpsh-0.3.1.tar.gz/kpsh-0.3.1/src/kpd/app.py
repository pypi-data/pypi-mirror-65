# SPDX-License-Identifier: GPL-3.0-or-later

# Copyright (C) 2019 Michał Góral.

import os
import sys
import argparse
import tempfile
import signal

from kpd.io import Interactive, NonInteractive, Daemon, Arguments

from kpd.db import DelayedPyKeePass
from kpd.commands import prepare_command_parser
from kpd._version import version


class Cleanup:
    def __init__(self):
        signal.signal(signal.SIGINT, self.sysexit)
        signal.signal(signal.SIGTERM, self.sysexit)

    def sysexit(self, signum, frame):
        raise SystemExit(signum)


def default_socket_path():
    tmp = tempfile.gettempdir()
    fname = 'kpsh-{}.sock'.format(os.getuid())
    return os.path.join(tmp, fname)


def prepare_args():
    ap = argparse.ArgumentParser(description='KeePass database shell access.')
    ap.add_argument('db', nargs='?', help='path to KeePass database.')

    ap.add_argument('--password', default=None,
        help='Database password.')
    ap.add_argument('--pw-cmd', default=None,
        help='Password will be obtained from the output of this command.')
    ap.add_argument('--keyfile', default=None,
        help='Key file for unlocking database.')
    ap.add_argument('--pinentry',
        help='Command used to run pinentry.')
    ap.add_argument('-c', '--command', action='append',
        help='Command to execute. If command contains spaces, it must be '
             'enclosed in double quotes. kpsh will be started in '
             'non-interactive mode.')
    ap.add_argument('--prompt', default='<style fg="ansiblue">{}</style>> ',
        help='Text used by shell for prompt.')
    ap.add_argument('-d', '--daemon', action='store_true',
        help='Start as daemon listening on a socket given by --socket-path')
    ap.add_argument('-s', '--socket-path', default=default_socket_path(),
        help='Path to the socket which will be created in daemon mode.')
    ap.add_argument('--version', action='version',
                    version='%(prog)s {}'.format(version))
    return ap.parse_args()


def main():
    cl = Cleanup()
    args = prepare_args()

    cmd_parser, parsers = prepare_command_parser()

    if args.command:
        ioh = Arguments(args.command)
    elif args.daemon:
        ioh = Daemon(args.socket_path)
    elif sys.stdin.isatty():
        ioh = Interactive(args.prompt, parsers)
    else:
        ioh = NonInteractive()

    kp = DelayedPyKeePass(args, ioh)
    return ioh.run(kp, cmd_parser)
