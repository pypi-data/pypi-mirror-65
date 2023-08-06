# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2019 Michał Góral.

_PLACEHOLDERS = {
    '{TITLE}'     : lambda e: e.title,
    '{USERNAME}'  : lambda e: e.username,
    '{URL}'       : lambda e: e.url,
    '{PASSWORD}'  : lambda e: e.password,
    '{NOTES}'     : lambda e: e.notes,
    '{PLUS}'      : lambda _: '+',
    '{PERCENT}'   : lambda _: '%',
    '{CARET}'     : lambda _: '^',
    '{TILDE}'     : lambda _: '~',
    '{LEFTPAREN}' : lambda _: '(',
    '{RIGHTPAREN}': lambda _: ')',
    '{LEFTBRACE}' : lambda _: '{',
    '{RIGHTBRACE}': lambda _: '}',
    '{AT}'        : lambda _: '@',
    '{+}'         : lambda _: '+',
    '{%}'         : lambda _: '%',
    '{^}'         : lambda _: '^',
    '{~}'         : lambda _: '~',
    '{(}'         : lambda _: '(',
    '{)}'         : lambda _: ')',
    '{[}'         : lambda _: '[',
    '{]}'         : lambda _: ']',
    '{{}'         : lambda _: '{',
    '{}}'         : lambda _: '}',
}

def replace_placeholder(entry, token):
    fn = _PLACEHOLDERS.get(token)
    if callable(fn):
        return fn(entry)
    return None

