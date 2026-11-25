#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auto-Awesome: run every osint-active module against the target."""

from core.methods.runall import run_category

info = "Launch all osint-active modules."
searchinfo = "ALL: osint-active"
properties = {}


def attack(web):
    run_category("osint-active", web)
