# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2019 Michał Góral.

import sys

def eprint(*a, **kw):
    kw['file'] = sys.stderr
    print(*a, **kw)

