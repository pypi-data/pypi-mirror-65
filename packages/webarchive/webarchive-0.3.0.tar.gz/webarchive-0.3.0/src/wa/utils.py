# SPDX-License-Identifier: GPL-3.0-or-later

# Copyright (C) 2020 Michał Góral.

import sys
import subprocess


def eprint(*a, **kw):
    kw['file'] = sys.stderr
    print(*a, **kw)


def safe_run(*a, **kw):
    class _EmptyCompletedProcess:
        args = None
        returncode = None
        stdout = ''
        stderr = ''

    try:
        return subprocess.run(*a, **kw)
    except OSError as e:
        eprint(e)
        return _EmptyCompletedProcess()
