#!/usr/bin/env python3
# Copyright (C) <2019> Association Prologin <association@prologin.org>
# SPDX-License-Identifier: GPL-3.0+

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gccsite.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
