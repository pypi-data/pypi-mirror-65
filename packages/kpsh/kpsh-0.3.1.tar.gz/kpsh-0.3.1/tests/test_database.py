import os
import pytest

from kpd.db import DelayedPyKeePass


@pytest.fixture
def dbargs(tmpdb, fakeargs):
    fakeargs.db = tmpdb('db_argon2_kdbx4_pass.kdbx')
    return fakeargs


def test_states(dbargs, iohandler):
    dbargs.password = 'foobar'
    kp = DelayedPyKeePass(dbargs, iohandler)
    assert kp.locked
    assert kp.unlock()
    assert not kp.locked


def test_fail_unlock(dbargs, iohandler):
    kp = DelayedPyKeePass(dbargs, iohandler)
    assert not kp.unlock()


def test_unlock_of_unlocked_db(dbargs, iohandler):
    iohandler.prompt.return_value = 'foobar'
    kp = DelayedPyKeePass(dbargs, iohandler)

    assert kp.unlock()

    iohandler.prompt.return_value = None
    assert kp.unlock()


def test_auto_reload(dbargs, iohandler):
    iohandler.prompt.return_value = 'foobar'
    kp = DelayedPyKeePass(dbargs, iohandler)

    assert kp.unlock()
    assert kp.kp

    # Let's change the passwords so we can verify that auto-reloading fails
    kp.kp.password = None
    iohandler.prompt.return_value = None

    # Modify mtime of our database
    curr = os.stat(dbargs.db)
    os.utime(dbargs.db, (curr.st_atime, curr.st_mtime + 100))

    assert not kp.kp  # failed auto-unlocking because we removed password

    iohandler.prompt.return_value = 'foobar'
    assert kp.kp
