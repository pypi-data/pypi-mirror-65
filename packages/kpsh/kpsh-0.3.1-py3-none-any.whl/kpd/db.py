# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2019 Michał Góral.

import os
import sys
import subprocess
import operator
import collections


class DatabaseError(Exception):
    pass

# Delays importing of PyKeePass which by itself adds ~150 ms to startup...
class DelayedPyKeePass:
    def __init__(self, args, ioh):
        self._db = None
        if args.db:
            self.change_db(args.db)

        self._password = args.password
        self._keyfile = args.keyfile

        self._pw_cmd = args.pw_cmd
        self._pinentry = args.pinentry

        self._kp = None
        self._mtime = None
        self._entries  = None

        self._ioh = ioh

    def _getpass(self):
        if self._password is not None:
            yield self._password
        if self._pw_cmd is not None:
            yield readpass(self._pw_cmd)
        if self._password is None and self._pw_cmd is None \
                and self._keyfile is not None:
            # password=None supports Composite Master Key with only a keyfile
            # https://keepass.info/help/base/keys.html
            yield None
        yield askpass(self._db, self._pinentry, self._ioh)

    def unlock(self):
        if self._kp and self._mtime == self._read_mtime():
            return True
        elif self._kp:
            # If e.g. database password was changed, this might fail. That's OK, 
            # but we must allow user to provide a password in a second,
            # "ordinary" database read.
            if self._read_db([self._kp.password], self._kp.keyfile):
                return True
            else:
                self._ioh.eprint(
                    'Database was modified externally and must be reloaded, '
                    'but auto-reload failed. Re-obtaining password.')

        if not self._db:
            self._ioh.eprint('No database is selected.')
            return False

        if not self._read_db(self._getpass, self._keyfile):
            self._ioh.eprint('Failed unlocking database {}.'.format(self._db))
            return False
        return True

    def lock(self):
        self._kp = None
        self._entries = None
        self._password = None
        self._keyfile = None

    def change_db(self, db):
        self.lock()
        if not os.path.isfile(db):
            self._ioh.eprint('Invalid database: \'{}\''.format(db))
            return
        self._db = db

    def change_credentials(self, password=None, keyfile=None):
        if not self.locked:
            raise DatabaseError(
                'Database must be locked before changing credentials '
                'used for unlocking.')

        self._password = password
        self._keyfile = keyfile

    @property
    def locked(self):
        return self._kp is None

    @property
    def db(self):
        return self._db

    @property
    def kp(self):
        self.unlock()
        return self._kp

    @property
    def entries(self):
        if not self.kp:
            return collections.OrderedDict()

        if self._entries is None:
            self._entries = collections.OrderedDict(
                (e.path, e)
                for e in sorted(self.kp.entries,
                                key=operator.attrgetter('path')))

        return self._entries

    @property
    def paths(self):
        return [e for e in self.entries.keys()]

    def iter_paths(self):
        for entry in self.entries:
            yield entry

    def _read_mtime(self):
        return os.stat(self._db).st_mtime

    def _read_db(self, password_iter, keyfile):
        from pykeepass import PyKeePass

        if callable(password_iter):
            password_iter = password_iter()

        kp = None
        for pw in password_iter:
            try:
                kp = PyKeePass(self._db, password=pw, keyfile=keyfile)
            except Exception as e:
                pass
            else:
                self._mtime = self._read_mtime()
                break

        self._kp = kp
        self._entries = None
        return kp is not None


def askpass(db, pinentry, ioh):
    if pinentry:
        return _askpass_pinentry(db, pinentry)
    return _askpass_prompt(ioh)


def readpass(cmd):
    cp = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if cp.returncode != 0 or not cp.stdout:
        return None
    return cp.stdout


def _askpass_pinentry(db, pinentry):
    pein = 'setdesc Enter password for {}\ngetpin\n'.format(db)
    cp = subprocess.run(pinentry, input=pein, capture_output=True,
                        text=True)

    if cp.returncode != 0 or not cp.stdout:
        return None

    lines = cp.stdout.splitlines()
    dlines = [line for line in lines if line.startswith ('D ')]
    if not dlines:
        return None

    passline = dlines[0]
    return passline.partition(' ')[-1]


def _askpass_prompt(ioh):
    return ioh.prompt('Password: ', is_password=True)
