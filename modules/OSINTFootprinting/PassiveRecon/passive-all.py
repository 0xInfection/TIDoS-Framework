#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Auto-Awesome: run every osint-passive module against the target."""

from core.methods.runall import run_category

info = "Launch all osint-passive modules."
searchinfo = "ALL: osint-passive"
properties = {}


def attack(web):
    run_category("osint-passive", web)
