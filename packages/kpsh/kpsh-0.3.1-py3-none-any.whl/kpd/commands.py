# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2019 Michał Góral.

import sys
import os
import argparse
import subprocess
import time
import fnmatch


class CommandError(Exception): pass
class ArgumentParserError(Exception): pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


def prepare_command_parser():
    cp = ThrowingArgumentParser(prog='', add_help=False)
    sp = cp.add_subparsers(required=True)

    parsers = {}
    parsers[None] = cp

    # helper function which automatically creates help-friendly parsers
    def add_parser(command, *a, **kw):
        kw['add_help'] = False

        descr = kw.get('description')
        if descr:
            kw['description'] = '{}\n\n{}'.format(kw['help'], descr)
        else:
            kw['description'] = kw['help']

        parser = sp.add_parser(command, *a, **kw)
        parsers[command] = parser
        return parser

    ######### open
    open_sp = add_parser('open', help='Change currently opened database.')
    open_sp.add_argument('filepath', help='path to database file.')
    open_sp.set_defaults(func=open_)

    ######### unlock
    unlock_sp = add_parser('unlock', help='Unlock currently opened database.')
    unlock_sp.add_argument('--keyfile', default='',
                           help='key file used for unlocking database')
    unlock_sp.set_defaults(func=unlock)

    ######### lock
    lock_sp = add_parser('lock', help='Lock a database.')
    lock_sp.set_defaults(func=lock)

    ######### db
    db_sp = add_parser('db', help='Query opened database info.')
    db_sp.set_defaults(func=db)

    ######### ls
    ls_sp = add_parser('ls', help='List contents of database.')
    ls_sp.add_argument('glob', nargs='?', default='*',
                       help='display only entries which match glob expression')
    ls_sp.set_defaults(func=ls)

    ######### show
    show_sp = add_parser('show', help='Show contents of entry.',
        description='Search is case-sensitive.')
    show_sp.add_argument('path', help='path which should be shown')
    show_sp.add_argument('fields', nargs='*',
        help='only display certain fields')
    show_sp.add_argument('-n', '--no-field-name', action='store_true',
        help='hide field name when printing entry fields.')
    show_sp.set_defaults(func=show)

    ######### autotype
    at_sp = add_parser('autotype', help='Auto-type sequence of entry fields.',
        description='This simulates keypresses to any currently open window. '
                    'It\'s particularily useful when kpsh is run from a script '
                    'or keypress in non-interactive mode (`-c` switch). If '
                    '`-s` is given, it will be used as auto-type sequence. '
                    'Otherwise sequence defined for selected entry will be '
                    'used or the default one if there is none (`-d`).')
    at_sp.add_argument('path', help='path of entry to auto-type')
    at_sp.add_argument('-s', '--sequence', help='override auto-type sequence')
    at_sp.add_argument('-d', '--default',
        default='{USERNAME}{TAB}{PASSWORD}{ENTER}',
        help='default auto-type sequence used when entry doesn\'t specify '
             'sequence itself.')
    at_sp.add_argument('-D', '--delay', type=int, default=40,
        help='delay beteen simulated keypresses')
    at_sp.add_argument('-f', '--force', action='store_true',
        help='force auto-type for entries for which auto-type was disabled')
    at_sp.set_defaults(func=autotype)

    ######### exit
    exit_sp = add_parser('exit', help='Exit shell.')
    exit_sp.set_defaults(func=exit)

    ######### echo
    echo_sp = add_parser('echo', help='Display a message.')
    echo_sp.add_argument('message', nargs='*', help='message to be displayed')
    echo_sp.set_defaults(func=echo)

    ######### sleep
    sleep_sp = add_parser('sleep', help='Sleep for a given number of seconds.',
        description='Seconds might be a floating number when fractions of '
                    'second are needed.')
    sleep_sp.add_argument('secs', type=float, help='seconds to sleep')
    sleep_sp.set_defaults(func=sleep)

    ######### help
    help_sp = add_parser('help', help='Show help for any message.')
    help_sp.add_argument('command', nargs='?')
    help_sp.set_defaults(func=lambda *a, parsers=parsers: help_(*a, parsers))

    return cp, parsers

def tokenize(seq):
    tokens = []

    i = 0
    while i < len(seq):
        start = seq.find('{', i)

        if start != -1:
            if i < start:
                tokens.append(seq[i:start])

            end = seq.find('}', start)
            nend = end + 1

            if end == -1:
                end = len(seq) - 1
            elif end == start + 1 and len(seq) > nend and seq[nend] == '}':  # {}}
                end = nend

            tokens.append(seq[start:end + 1])
            i = end + 1
        else:
            tokens.append(seq[i:])
            i = len(seq)

    return tokens


def xdotool(*args):
    cmd = ['/usr/bin/xdotool']
    cmd.extend(args)
    subprocess.run(cmd)


def autotype(kp, args, ioh):
    from kpd.autotype.xdotoolkeys import XDOTOOL_KEYS
    from kpd.autotype.placeholders import replace_placeholder
    from kpd.autotype.commands import run_command

    delay = str(args.delay)
    entry = _get(args.path, kp)

    if not entry.autotype_enabled and not args.force:
        ioh.eprint('Autotype disabled for {}. '
                   'Use -f to force autotype.'.format(args.path))
        return

    sequence = args.sequence if args.sequence else entry.autotype_sequence
    if not sequence:
        sequence = args.default

    for token in tokenize(sequence):
        if token.startswith('{') and token.endswith('}'):
            if run_command(token):
                continue

            placeholder = replace_placeholder(entry, token)
            if placeholder is not None:
                xdotool('type', '--delay', delay, '--', placeholder)
                continue

            specialkey = XDOTOOL_KEYS.get(token)
            if specialkey is not None:
                xdotool('key', '--clearmodifiers', '--delay', delay, specialkey)
                continue

            ioh.eprint('Unsupported keyword: {}'.format(token))
        else:
            xdotool('type', '--delay', delay, '--', token)


def show(kp, args, ioh):
    entry = _get(args.path, kp)
    attrs = ['path', 'username', 'password', 'url', 'autotype_sequence',
              'notes']

    for attr in attrs:
        if args.fields and attr not in args.fields:
            continue
        val = getattr(entry, attr)
        if val is None:
            continue

        if args.no_field_name:
            ioh.print(val)
        else:
            ioh.print('{}: {}'.format(attr, val))


def echo(kp, args, ioh):
    ioh.print(*args.message)


def sleep(kp, args, ioh):
    time.sleep(args.secs)


def ls(kp, args, ioh):
    for path in fnmatch.filter(kp.iter_paths(), args.glob):
        ioh.print(path)


def help_(kp, args, ioh, parsers):
    parser = parsers.get(args.command)
    if parser is None:
        ioh.eprint('no such command: {}'.format(args.command))
        parser = parsers.get(None)

    parser.print_help()


def exit(kp, args, ioh):
    ioh.stop()


def open_(kp, args, ioh):
    fp = os.path.expanduser(args.filepath)
    kp.change_db(fp)


def unlock(kp, args, ioh):
    if not kp.locked:
        return

    kf = os.path.expanduser(args.keyfile) if args.keyfile else None
    kp.change_credentials(keyfile=kf)
    kp.unlock()


def lock(kp, args, ioh):
    kp.lock()


def db(kp, args, ioh):
    ioh.print(kp.db)
    ioh.print('Locked: {}'.format(kp.locked))


def _get(path, kp):
    entry = kp.entries.get(path)
    if not entry:
        raise CommandError('entry not found: {}'.format(path))
    return entry
