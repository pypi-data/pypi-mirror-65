# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2019 Michał Góral.

import time
import re

def _token_delay(token):
    match = re.match(r'{DELAY (\d+)}', token)
    if match:
        delay = match.group(1)
        return lambda t=delay: time.sleep(int(t) / 1000)
    return None

_COMMANDS = [
    _token_delay,
]

def run_command(token):
    for checker in _COMMANDS:
        cmd = checker(token)
        if callable(cmd):
            cmd()
            return True
    return False

