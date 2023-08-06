import os
import shutil
from unittest.mock import Mock
import pytest

from kpd.io import Handler

@pytest.fixture
def tmpdb(tmpdir):
    curdir = os.path.dirname(os.path.abspath(__file__))

    keysrc = os.path.join(curdir, 'db', 'keyfile')
    keydst = os.path.join(str(tmpdir), 'keyfile')
    shutil.copy(keysrc, keydst)

    def _f(name):
        src = os.path.join(curdir, 'db', name)
        dst = os.path.join(str(tmpdir), name)
        shutil.copy(src, dst)
        return dst
    return _f


@pytest.fixture
def fakeargs():
    class Args:
        def __getattr__(self, name):
            return self.__dict__.get(name, None)

    return Args()


@pytest.fixture
def iohandler():
    class ProggrammableIO(Handler):
        def __init__(self):
            self.prompt = Mock()
            self.get_command = Mock()
            super().__init__()

    return ProggrammableIO()
