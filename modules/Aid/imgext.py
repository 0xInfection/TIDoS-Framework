#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Image analysis -- read EXIF metadata (and GPS coordinates) from an image."""

from __future__ import annotations

import os

from core.methods import modkit as kit

info = ("Forensic image analysis: extracts EXIF metadata from an image and, when "
        "present, decodes the GPS coordinates to decimal latitude/longitude. "
        "Set PATH to run non-interactively. Requires Pillow.")
searchinfo = "Image Analysis"
properties = {"PATH": ["Path to the image file (empty: prompt)", ""]}


def _ratio(value) -> float:
    """A single EXIF rational -> float (modern Pillow gives IFDRational)."""
    try:
        return float(value)
    except (TypeError, ValueError):
        num, den = value
        return num / den if den else 0.0


def gps_coordinates(gps: dict):
    """(lat, lng) in decimal degrees from a GPSInfo dict, or None."""
    try:
        lat_ref, lat = gps[1], gps[2]
        lng_ref, lng = gps[3], gps[4]
    except (KeyError, TypeError):
        return None
    lat_ref = lat_ref.decode() if isinstance(lat_ref, bytes) else str(lat_ref)
    lng_ref = lng_ref.decode() if isinstance(lng_ref, bytes) else str(lng_ref)

    def to_degrees(dms):
        d, m, s = (_ratio(x) for x in dms)
        return d + m / 60.0 + s / 3600.0

    lat_deg = to_degrees(lat) * (-1 if lat_ref.upper().startswith("S") else 1)
    lng_deg = to_degrees(lng) * (-1 if lng_ref.upper().startswith("W") else 1)
    return lat_deg, lng_deg


def read_exif(path: str) -> dict:
    """{tag name: value} of an image's EXIF, GPSInfo kept raw for decoding."""
    from PIL import Image
    from PIL.ExifTags import TAGS

    with Image.open(path) as image:
        raw = getattr(image, "_getexif", lambda: None)()
    if not raw:
        return {}
    return {TAGS.get(tag, tag): value for tag, value in raw.items()}


def imgext(path: str):
    if not os.path.isfile(path):
        kit.bad(f"No such file: {path}")
        return
    try:
        exif = read_exif(path)
    except ImportError:
        kit.bad("Pillow is not installed: pip install pillow (see docs/install.md).")
        return
    except Exception as e:
        kit.bad(f"Could not read image: {type(e).__name__}: {e}")
        return
    if not exif:
        kit.warn("No EXIF metadata found in this image.")
        return

    kit.info(f"EXIF metadata for {path}:")
    gps = exif.pop("GPSInfo", None)
    kit.kv_table((tag, value) for tag, value in sorted(exif.items(), key=lambda kv: str(kv[0])))
    if isinstance(gps, dict):
        coords = gps_coordinates(gps)
        if coords:
            lat, lng = coords
            kit.found("GPS", f"{lat:.6f}, {lng:.6f}")
            kit.found("Map", f"https://maps.google.com/?q={lat:.6f},{lng:.6f}")
    kit.good("Image analysis done.")


def attack(web):
    path = kit.option(properties, "PATH", "Enter the path to the image")
    if not path:
        kit.bad("No path given; set PATH or run interactively.")
        return
    imgext(path)
