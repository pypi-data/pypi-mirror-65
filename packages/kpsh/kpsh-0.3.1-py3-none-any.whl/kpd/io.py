import os
import sys
import shlex
from functools import lru_cache
from contextlib import contextmanager
import socket
import struct
import select

from prompt_toolkit import PromptSession
from prompt_toolkit import prompt as input_prompt
from prompt_toolkit.formatted_text.html import HTML

from kpd.commands import CommandError, ArgumentParserError
from kpd.completion import CommandCompleter

class Handler:
    def __init__(self):
        self._run = True
        self._returncode = 0

    def prompt(self, prompt='', is_password=False):
        '''Used to prompt for any kind of input'''
        return None

    def print(self, *a, **kw):
        '''Used to print ordinary messages'''
        print(*a, **kw)

    def eprint(self, *a, **kw):
        '''Used to print error messages'''
        kw['file'] = sys.stderr
        print(*a, **kw)

    def get_command(self, kp):
        '''Called when handler is ready to accept a next command. Returns a
        unparsed argument-like string. Children should override this method to
        read user input.'''
        return None

    def finalize_command(self):
        '''Always called after each command ends.'''
        pass

    def initialize(self, kp):
        '''Called before Handler enters its command loop.'''
        pass

    def teardown(self, kp):
        '''Called after Handler exits its command loop.'''
        pass

    def stop(self, returncode=0):
        '''Used to stop the running command loop.'''
        self._run = False
        self._returncode = returncode

    def run(self, kp, cmd_parser):
        with self._setup(kp):
            while self._run:
                text = self.get_command(kp)
                if not text:
                    continue

                cmd = shlex.split(text)
                if not cmd:
                    continue

                try:
                    cargs = cmd_parser.parse_args(cmd)
                    cargs.func(kp, cargs, self)
                except ArgumentParserError as e:
                    self.eprint(str(e))
                except CommandError as e:
                    self.eprint(str(e))
                finally:
                    self.finalize_command()
        return self._returncode

    @contextmanager
    def _setup(self, kp):
        self.initialize(kp)
        try:
            yield
        except KeyboardInterrupt:
            self.stop(1)
        finally:
            self.teardown(kp)


class Interactive(Handler):
    def __init__(self, prompt, parsers):
        self._session = None
        self._prompt = prompt
        self._parsers = parsers
        super().__init__()

    def initialize(self, kp):
        compl = CommandCompleter(kp, (p for p in self._parsers if p))
        self._session = PromptSession(completer=compl,
                                      complete_while_typing=False)

    def get_command(self, kp):
        try:
            return self._session.prompt(self._ps1(kp.db))
        except KeyboardInterrupt:
            return None
        except EOFError:
            self.stop()
            return None

    def prompt(self, prompt='', is_password=False):
        try:
            return input_prompt(prompt, is_password=is_password)
        except (EOFError, KeyboardInterrupt):
            return None

    @lru_cache(maxsize=32)
    def _ps1(self, dbpath):
        if not dbpath:
            dbpath = ''
        home = os.path.expanduser('~')
        if dbpath.startswith(home):
            dbpath = dbpath.replace(home, '~')

        return HTML(self._prompt.format(dbpath))


class NonInteractive(Handler):
    def __init__(self):
        self._read_input = False
        super().__init__()

    def get_command(self, kp):
        try:
            return input()
        except EOFError:
            self.stop()
            return None


class Arguments(Handler):
    def __init__(self, commands):
        self._iter = iter(commands)
        super().__init__()

    def get_command(self, kp):
        try:
            return next(self._iter)
        except StopIteration:
            self.stop()
            return None


class Daemon(Handler):
    def __init__(self, path):
        self._path = path
        super().__init__()

    def initialize(self, kp):
        self._serv = _SocketServer(self._path)

    def teardown(self, kp):
        self._serv.stop()

    def prompt(self, prompt='', is_password=False):
        if is_password:
            resptype = 'PS'
        else:
            resptype = 'P'

        msg = '{} {}'.format(resptype, prompt)
        self._send(msg)
        return self._recv()

    def print(self, *a, **kw):
        msg = 'M {}'.format(' '.join(str(arg) for arg in a))
        self._send(msg)

    def eprint(self, *a, **kw):
        msg = 'E {}'.format(' '.join(a))
        self._send(msg)

    def get_command(self, kp):
        return self._recv()

    def finalize_command(self):
        self._send('OK')

    def _recv(self):
        buf = self._serv.recv(4)
        if not buf:
            return None

        msglen = struct.unpack("!i", buf)[0]
        if msglen == 0:
            return None

        data = self._serv.recv(msglen)
        if not data:
            return None

        return data.decode()

    def _send(self, msg):
        data = msg.encode()
        msglen = struct.pack('!i', len(data))
        self._serv.send(msglen)
        self._serv.send(data)


class _SocketServer:
    '''Wrapper for all hairy socket stuff'''

    def __init__(self, path):
        self._remove_socket(path)
        self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._sock.bind(path)
        self._sock.listen(1)
        self._conn = None

    def send(self, msg):
        if not self._conn:
            return

        msglen = len(msg)
        totalsent = 0
        while totalsent < msglen:
            try:
                sent = self._conn.send(msg[totalsent:msglen])
            except BrokenPipeError:
                sent = 0

            if sent == 0:
                self._close_conn()
                return
            totalsent += sent

    def recv(self, size):
        self._wait_for_client()
        buf = self._conn.recv(size)
        if not buf:
            self._close_conn()
            return None
        return buf

    def stop(self):
        self._close_conn()

        if self._sock:
            self._sock.shutdown(socket.SHUT_RDWR)
            self._sock.close()
            self._sock = None

    def _accept(self):
        conn, _ = self._sock.accept()
        return conn

    def _wait_for_client(self):
        if not self._conn:
            self._conn = self._accept()

        while True:
            # Server continuously accepts all connections because queuing them
            # on listen() is unreliable - it's impossible to tell how listen(0)
            # behaves. Certainly it queues at least 1 non-accepted connection,
            # which might block clients forever. So we'll just wait on
            # select() whenever blocking socket operation occurs and close all
            # connections but the first one. Clients should notice broken
            # connection with first recv().
            readable, _, _ = select.select([self._conn, self._sock], [], [])
            if self._sock in readable:
                self._accept().close()
            if self._conn in readable:
                break

    def _close_conn(self):
        if not self._conn:
            return

        self._conn.close()
        self._conn = None

    def _remove_socket(self, path):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
