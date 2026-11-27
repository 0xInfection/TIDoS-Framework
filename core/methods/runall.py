#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Run every module of a category against one target (the *-all modules)."""

import importlib

from core.methods import modkit as kit


def run_category(category: str, target) -> None:
    from core.methods.select import list as list_modules

    names = [m for m in list_modules(category, False) if not m.endswith("-all")]
    failed = []
    for i, name in enumerate(names, 1):
        short = name.rsplit(".", 1)[-1]
        kit.info(f"[{i}/{len(names)}] {short}")
        try:
            importlib.import_module(name).attack(target)
        except KeyboardInterrupt:
            kit.warn(f"{short} interrupted, moving on (Ctrl+C again to abort).")
        except Exception as e:
            kit.bad(f"{short} failed on {kit.url(target)}: {e}")
            failed.append(short)
    kit.good(f"{category}: {len(names) - len(failed)}/{len(names)} modules completed")
    if failed:
        kit.bad("Failed: " + ", ".join(failed))
