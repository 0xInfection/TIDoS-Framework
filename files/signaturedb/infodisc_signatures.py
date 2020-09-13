#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
# -:-:-:-:-:-:-:-:-:-:-:-:#

# Author: @_tID
# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

EMAIL_HARVESTER_SIGNATURE = r'''[-a-zA-Z0-9._]+@[-a-zA-Z0-9_]+.[a-zA-Z0-9_.]+'''
PHONE_NUMBER_SIGNATURE = r'''\+\d{2}\s?0?\d{10}'''
INTERNAL_IP_SIGNATURE = r'''/(^127\.)|(^192\.168\.)|(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^::1$)|(^[fF][cCdD])/'''
SOCIAL_SECURITY_SIGNATURE = r'''(((?!000)(?!666)(?:[0-6]\d{2}|7[0-2][0-9]|73[0-3]|7[5-6][0-9]|77[0-2]))-((?!00)\d{2})-((?!0000)\d{4}))'''
VISA_MASTERCARD_SIGNATURE = r'''^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})$'''
AMEX_CARD_SIGNATURE = r"""^3[47][0-9]{13}$"""
EXPRESS_CARD_SIGNATURE = r'''^[34|37][0-9]{14}$'''
DISCOVER_CARD_SIGNATURE = r"""^6(?:011|5[0-9]{2})[0-9]{12}$"""
MASTERCARD_SIGNATURE = r'''^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$'''
VISA_SIGNATURE = r"""^4[0-9]{12}(?:[0-9]{3})?$"""
