#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""
XPath error signatures: (label, case-insensitive regex).

Only messages that XPath engines emit for a malformed expression. Generic
XML-parser and COM errors (libxml2 failures, 80004005, "exactly one root
element") were dropped. The scanner additionally requires the signature to
be absent from the baseline responses.
"""

XPATH_ERRORS = [
    (".NET XPathException", r"System\.Xml\.XPath\.XPathException"),
    (".NET MS.Internal.Xml", r"MS\.Internal\.Xml\.XPath"),
    (".NET token", r"(?:'[^']{0,80}' has an invalid token|Expected token '[\])]')"),
    ("Java XPathExpressionException", r"javax\.xml\.xpath\.XPathExpressionException"),
    ("Xalan", r"org\.apache\.xpath\.(?:XPath|compiler)\w*|com\.sun\.org\.apache\.xpath"),
    ("Saxon", r"net\.sf\.saxon\.(?:trans|s9api)\.\w*Exception|XPST0003"),
    ("PHP DOMXPath", r"DOMXPath::(?:query|evaluate)\(\)[^<\n]{0,80}(?:Invalid expression|Invalid predicate|Unfinished literal)"),
    ("PHP SimpleXML xpath", r"SimpleXMLElement::xpath\(\)[^<\n]{0,80}Invalid"),
    ("libxml2 XPath", r"XPath error\s*:?\s*(?:Invalid (?:expression|predicate)|Unfinished literal|"
                      r"Undefined namespace prefix|Invalid number of arguments)"),
    ("lxml XPathEvalError", r"lxml\.etree\.XPath(?:Eval|Syntax)Error|XPath(?:Eval|Syntax)Error"),
    ("Python ElementTree", r"SyntaxError: (?:invalid predicate|prefix .{1,40} not found in prefix map)"),
    ("XPathException", r"\bXPathException\b"),
    ("Unknown error in XPath", r"Unknown error in XPath"),
    ("XPATH syntax error", r"XPATH syntax error"),
    ("MSXML", r"msxml\d?\.dll[^<\n]{0,80}(?:expected|unfinished|token)"),
    ("XPath operand", r"An operand in Union Expression does not produce a node-set|"
                      r"Expected node test or name specification after axis operator|"
                      r"Document Axis does not allow any context Location Steps|"
                      r"Empty (?:Path|Relative Location Path|Union) Expression"),
    ("Lotus Notes", r"Notes error: Query is not understandable"),
]
