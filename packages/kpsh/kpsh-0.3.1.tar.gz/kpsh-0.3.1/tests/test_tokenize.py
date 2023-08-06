import pytest

from kpd.commands import tokenize

@pytest.mark.parametrize('sequence,tokens', [
    ('', []),
    ('abc', ['abc']),
    ('{USER}{TAB}{PASSWORD}{ENTER}', ['{USER}', '{TAB}', '{PASSWORD}', '{ENTER}']),
    ('abc{USER}', ['abc', '{USER}']),
    ('{USER}def', ['{USER}', 'def']),
    ('abc{USER}def', ['abc', '{USER}', 'def']),
    ('abc{USER}def{USER}', ['abc', '{USER}', 'def', '{USER}']),
    ('{}', ['{}']),
    ('{{}', ['{{}']),
    ('{}}', ['{}}']),
    ('{DELAY 5}', ['{DELAY 5}']),
    ('{USERNAME}{{}{PASSWORD}', ['{USERNAME}', '{{}', '{PASSWORD}']),
    ('{{{{{', ['{{{{{']),
    ('}}}}}', ['}}}}}']),
    ('{abc{def', ['{abc{def']),
    ('{abc{def}', ['{abc{def}']),
    ('{abc}def}', ['{abc}', 'def}']),
])
def test_tokenize(sequence, tokens):
    assert tokens == tokenize(sequence)

