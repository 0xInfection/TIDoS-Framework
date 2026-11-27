#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Auto-Awesome: run every vulnerability analysis module against the target."""

from core.methods.runall import run_category

info = "Launch all vlnysis modules."
searchinfo = "ALL: vlnysis"
properties = {}


def attack(web):
    run_category("vlnysis", web)
