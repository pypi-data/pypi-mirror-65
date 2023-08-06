import os
import glob
import re

from prompt_toolkit.completion import Completer, Completion

_OPT_PATTERN = re.compile(r'([a-zA-Z0-9_]+|[^a-zA-Z0-9_\s]+)')

class CommandCompleter(Completer):
    def __init__(self, kp, commands):
        self._commands = sorted(commands)
        self._kp = kp

    def get_completions(self, document, complete_event):
        text_before = document.text_before_cursor
        if ' ' in text_before:
            command = text_before.partition(' ')[0]
            fn = getattr(self, '_{}'.format(command), None)
            if callable(fn):
                yield from fn(document)
        else:
            yield from self._complete_commands(document)

    def _complete_commands(self, document):
        text_before = document.text_before_cursor
        for command in self._commands:
            if command.startswith(text_before):
                yield Completion(command, -len(text_before))

    def _show(self, document):
        opts = ['--no-field-name']
        yield from self._path_and_opts(document, opts)

    def _autotype(self, document):
        opts = ['--default::change default sequence',
                '--sequence::override sequence',
                '--force::force auto-type when disabled',
                '--delay::delay between keypresses']
        yield from  self._path_and_opts(document, opts)

    def _help(self, document):
        word = document.get_word_before_cursor()
        for command in self._commands:
            if command.startswith(word):
                yield Completion(command, -len(word))

    def _open(self, document):
        yield from self._filepath(document)

    def _path_and_opts(self, document, opts):
        word = document.get_word_before_cursor(WORD=True)
        if word.startswith('-'):
            completions = sorted(opts)
        else:
            completions = self._kp.paths if not self._kp.locked else []

        for compl in completions:
            compl, _, meta = compl.partition('::')
            if not meta:
                meta = None
            if compl.startswith(word):
                yield Completion(compl, -len(word), display_meta=meta)

    def _filepath(self, document):
        word = document.get_word_before_cursor(WORD=True)

        home = os.path.expanduser('~')
        tilde_repl = word.startswith('~/')
        for compl in glob.iglob('{}*'.format(os.path.expanduser(word))):
            meta = None
            if os.path.isfile(compl):
                meta = 'file'
            elif os.path.isdir(compl):
                meta = 'dir'

            if tilde_repl:
                compl = compl.replace(home, '~')

            yield Completion(compl, -len(word), display_meta=meta)
