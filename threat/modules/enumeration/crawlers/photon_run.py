#!/usr/bin/env python

from os import path
import sys
sys.path.append(path.abspath('lib/Photon'))

from lib.Photon.photon import photon

# menu 4

def photon_run(target):
    # from core.build_menu import buildmenu
    print('PHOTON RUN', photon)

