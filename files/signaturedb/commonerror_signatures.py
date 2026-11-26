#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""
Server-side error / debug-page signatures (used by the `errors` module).

SIGNATURES is a list of (technology, regex). Regexes are matched
case-insensitively against raw page bodies, so keep them specific enough
not to fire on ordinary prose.
"""

SIGNATURES = [
    # ---- PHP --------------------------------------------------------------
    ("PHP", r"<b>(?:Fatal error|Parse error|Warning|Notice|Deprecated)</b>:\s.{0,300}? on line <b>\d+</b>"),
    ("PHP", r"(?:Fatal error|Parse error|Warning|Notice):\s.{0,200}? in (?:<b>)?/[^<\s]+\.php(?:</b>)? on line (?:<b>)?\d+"),
    ("PHP", r"(?:PHP )?Fatal error:\s*(?:</b>\s*)?Uncaught \w+(?:\\\w+)*(?:Exception|Error)\b"),
    ("PHP", r"thrown in <b>"),
    ("PHP", r"open_basedir restriction in effect"),
    ("PHP", r"Warning: opendir\(Array\):"),
    ("PHP", r"<b>warning</b>[/]\w/\w/\S*"),
    ("PHP (Laravel)", r"Whoops, looks like something went wrong|Illuminate\\(?:Database|Foundation|Routing)\\"),
    ("PHP (Laravel Ignition)", r"window\.ignite\(|Spatie\\\\(?:Ignition|LaravelIgnition)"),
    ("PHP (Symfony)", r"Symfony\\Component\\[A-Za-z\\]+Exception|<abbr title=\"Symfony\\"),
    ("PHP (CodeIgniter)", r"A PHP Error was encountered|<h4>A Database Error Occurred</h4>"),
    ("PHP (Yii)", r"yii\\(?:base|db|web)\\\w*Exception"),
    ("PHP (Zend/Laminas)", r"(?:Zend|Laminas)\\[A-Za-z\\]+\\Exception"),

    # ---- ASP / ASP.NET / IIS ---------------------------------------------
    ("ASP.NET", r"Server Error in '[^']*' Application"),
    ("ASP.NET", r"<b>\s*Description:\s*</b>\s*An unhandled exception occurred during the execution of the"),
    ("ASP.NET", r"\[(?:HttpException|NullReferenceException|SqlException|InvalidOperationException)[^\]]*\]"),
    ("ASP.NET", r"ASP\.NET is configured to show verbose error messages"),
    ("ASP.NET", r"Version Information:</b>\s*Microsoft \.NET Framework Version:"),
    ("ASP.NET Core", r"An unhandled exception occurred while processing the request\.|Microsoft\.AspNetCore\.[\w.]+Exception:"),
    ("Classic ASP", r"<font face=\"Arial\" size=2>error '800a[0-9a-f]{4}'</font>"),
    ("Classic ASP", r"Active Server Pages</font> <font face=\"Arial\" size=2>error 'ASP \d+'"),
    ("Classic ASP", r"Server\.Execute Error|Server object error"),
    ("Classic ASP", r"<h2> <i>Runtime Error</i> </h2></span>"),
    ("IIS", r"<h2 style=\"font:8pt/11pt verdana; color:000000\">HTTP 403\.6 - Forbidden: IP address rejected"),
    ("IIS", r"Detailed Error Information:.{0,400}?Physical Path"),

    # ---- Java ---------------------------------------------------------------
    ("Java", r"\bat (?:java|javax|jakarta|sun)\.[\w$.]+\([\w$]+\.java:\d+\)"),
    ("Java", r"(?:java|javax|jakarta)\.\w+(?:\.\w+)*(?:Exception|Error):"),
    ("Java (Tomcat)", r"at org\.apache\.(?:catalina|coyote|jasper)\."),
    ("Java (Tomcat)", r"<h3>Apache Tomcat/[\d.]+</h3>|<title>Apache Tomcat/[\d.]+ - Error report</title>"),
    ("Java (Spring)", r"Whitelabel Error Page"),
    ("Java (Spring)", r"org\.springframework\.[\w.]+(?:Exception|Error)"),
    ("Java (Struts)", r"org\.apache\.struts2?\.[\w.]+Exception"),
    ("Java (JBoss/WildFly)", r"org\.jboss\.[\w.]+Exception|JBWEB\d{6}"),
    ("Java (Hibernate)", r"org\.hibernate\.[\w.]+Exception"),
    ("Java (generic)", r"<H3>Original Exception: </H3>|<H1>Error page exception</H1>"),

    # ---- ColdFusion ---------------------------------------------------------
    ("ColdFusion", r"<TR><TD><H4>Error Diagnostic Information</H4>"),
    ("ColdFusion", r"<title>Error Occurred While Processing Request</title>"),
    ("ColdFusion", r"coldfusion\.(?:runtime|sql|tagext)\.\w+"),
    ("ColdFusion", r"The error occurred in <b>[^<]+\.cfm"),

    # ---- Python ---------------------------------------------------------------
    # a real trace has a frame line; doctest examples in docs do not
    ("Python", r"Traceback \(most recent call last\):\s*(?:<br\s*/?>\s*)?File (?:\"|&quot;|&#34;)"),
    ("Python", r"<h2>Traceback <span>\(innermost last\)</span></h2>"),
    ("Python", r"exceptions\.ValueError|invalid literal for int\(\) with base"),
    ("Python (Django)", r"You're seeing this error because you have <code>DEBUG = True</code>"),
    ("Python (Django)", r"<th>Django Version:</th>|django\.(?:db|core|template)\.\w+\.\w*(?:Error|Exception)"),
    ("Python (Flask/Werkzeug)", r"Werkzeug Debugger|The debugger caught an exception in your WSGI application"),
    ("Python (FastAPI/Starlette)", r"starlette\.\w+\.\w*(?:Error|Exception)"),

    # ---- Ruby -------------------------------------------------------------
    ("Ruby on Rails", r"<h1 class=\"error_title\">Ruby on Rails application could not be started</h1>"),
    ("Ruby on Rails", r"Action Controller: Exception caught|ActionView::Template::Error|ActiveRecord::\w+Error"),
    ("Ruby (Sinatra)", r"Sinatra doesn(?:'|&#39;)t know this ditty"),
    ("Ruby", r"onclick=\"toggle\('full exception chain stacktrace'\)"),

    # ---- Node.js ---------------------------------------------------------
    ("Node.js", r"\bat (?:Object\.|Module\.|Function\.)?\S+ \((?:/|[A-Z]:\\)[^)]+\.(?:js|mjs|cjs|ts):\d+:\d+\)"),
    ("Node.js (Express)", r"<pre>(?:Error|TypeError|ReferenceError): .{0,200}?<br> &nbsp; &nbsp;at "),
    ("Node.js (Next.js)", r"\"(?:err|error)\":\{\"name\":\"\w*Error\",\"(?:source|message)\""),

    # ---- Go / Perl / misc -----------------------------------------------
    ("Go", r"goroutine \d+ \[running\]:|panic: runtime error:"),
    ("Perl", r"at /[\w/.-]+\.p[lm] line \d+\.|<h1>Software error:</h1>"),
    ("SSI", r"\[an error occurred while processing this directive\]"),
    ("CGI", r"<TITLE>nwwcgi Error"),
    ("Generic", r"<TITLE>500 Internal Server Error</TITLE>"),
    ("Generic", r"\bStack trace:\s*(?:<br\s*/?>)?\s*#0 "),

    # ---- Database errors ------------------------------------------------
    ("MySQL", r"You have an error in your SQL syntax|MySql\.Data\.MySqlClient\.MySqlException|com\.mysql\.jdbc\.exceptions\."),
    ("MySQL", r"Warning: mysqli?_\w+\(\)|SQLSTATE\[\w+\]: [^<]{0,120}MySQL"),
    ("PostgreSQL", r"PostgreSQL query failed|Warning:\s*pg_\w+\(\)|ERROR:\s+syntax error at or near \""),
    ("PostgreSQL", r"org\.postgresql\.util\.PSQLException|Npgsql\.\w+Exception"),
    ("MSSQL", r"Microsoft OLE DB Provider for (?:SQL Server|ODBC Drivers)|Unclosed quotation mark after the character string"),
    ("MSSQL", r"System\.Data\.SqlClient\.SqlException|\[Microsoft\]\[(?:ODBC )?SQL Server[^\]]*\]"),
    ("Oracle", r"\bORA-\d{5}: |quoted string not properly terminated|oracle\.jdbc\.\w+\.\w*Exception"),
    ("SQLite", r"SQLite(?:3)?::(?:query|SQLException)|sqlite3\.OperationalError: |SQLITE_ERROR\]?: "),
    ("DB2", r"\bDB2 SQL error:|SQLCODE=-\d+"),
    ("MongoDB", r"\bMongo(?:Server)?Error: |E11000 duplicate key error"),
    ("Generic SQL", r"SQLSTATE\[\w+\]: |\bPDOException(?:: | in /)|Syntax error in (?:string in )?query expression"),
]

# Backwards compatibility: older code imported a flat tuple of patterns.
patterns = tuple(rx for _, rx in SIGNATURES)
