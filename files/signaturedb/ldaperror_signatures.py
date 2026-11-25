#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LDAP error signatures: (label, case-insensitive regex).

Only messages that LDAP client libraries emit for a malformed search filter
or DN. Generic phrases ("Object does not exist", "Unknown error occurred",
"The syntax is invalid"...) were dropped: they appear on ordinary pages.
The scanner additionally requires the signature to be absent from the
baseline responses.
"""

LDAP_ERRORS = [
    ("PHP ldap_search", r"ldap_(?:search|list|read|bind)\(\)[^<\n]{0,80}(?:bad search filter|"
                        r"invalid dn syntax|filter error|search: )"),
    ("PHP ldap resource", r"supplied argument is not a valid ldap"),
    ("Java InvalidSearchFilter", r"javax\.naming\.directory\.InvalidSearchFilterException"),
    ("Java InvalidName", r"javax\.naming\.InvalidNameException"),
    ("Java NameNotFound", r"javax\.naming\.NameNotFoundException"),
    ("JNDI LDAP", r"com\.sun\.jndi\.ldap\.\w+"),
    ("UnboundID/Novell LDAPException", r"(?:com\.unboundid|com\.novell)\.ldap\.\w*LDAPException"),
    ("LDAPException", r"LDAPException\b[^<\n]{0,80}(?:filter|DN|syntax|parenthes)"),
    ("Bad search filter", r"\bbad search filter\b"),
    ("Unbalanced parenthesis", r"unbalanced parenthes[ie]s[^<\n]{0,40}filter|filter[^<\n]{0,60}unbalanced parenthes"),
    (".NET DirectoryServices", r"System\.DirectoryServices(?:\.Protocols)?\.(?:DirectoryServicesCOMException|LdapException)"),
    (".NET invalid filter", r"The (?:search filter|filter) (?:is invalid|is incorrect|cannot be recognized)"),
    ("Invalid DN syntax", r"\binvalid DN syntax\b"),
    ("python-ldap", r"ldap\.FILTER_ERROR|ldap3\.core\.exceptions\.LDAP\w+"),
    ("Net::LDAP", r"Net::LDAP::Filter"),
    ("Zope LDAPMultiPlugins", r"Products\.LDAPMultiPlugins"),
    ("IPWorks LDAP", r"IPWorksASP\.LDAP"),
]
