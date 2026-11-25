#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auto-Awesome: run every scanning & enumeration module against the target."""

from core.methods.runall import run_category

info = "Launch all scan modules."
searchinfo = "ALL: scan"
properties = {}


def attack(web):
    run_category("scan", web)
