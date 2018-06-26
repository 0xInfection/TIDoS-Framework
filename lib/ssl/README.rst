ssl
===

The old socket.ssl() support for TLS over sockets is being
superseded in Python 2.6 by a new 'ssl' module.  This package
brings that module to older Python releases, 2.3.5 and up (it may
also work on older versions of 2.3, but we haven't tried it).

It's quite similar to the 2.6 ssl module.  There's no stand-alone
documentation for this package; instead, just use the development
branch documentation for the SSL module at
http://docs.python.org/dev/library/ssl.html.

Version 1.0 had a problem with Python 2.5.1 -- the structure of
the socket object changed from earlier versions.

Version 1.1 was missing various package metadata information.

Version 1.2 added more package metadata, and support for
ssl.get_server_certificate(), and the PEM-to-DER encode/decode
routines.  Plus integrated Paul Moore's patch to setup.py for
Windows.  Plus added support for asyncore, and asyncore HTTPS
server test.

Version 1.3 fixed a bug in the test suite.

Version 1.4 incorporated use of -static switch.

Version 1.5 fixed bug in Python version check affecting build on
Python 2.5.0.

Version 1.7 (and 1.6) fixed some bugs with asyncore support (recv and
send not being called on the SSLSocket class, wrong semantics for
sendall).

Version 1.8 incorporated some code from Chris Stawarz to handle
sockets which are set to non-blocking before negotiating the SSL
session.

Version 1.9 makes ssl.SSLError a subtype of socket.error.

Version 1.10 fixes a bug in sendall().

Version 1.11 includes the MANIFEST file, and by default will turne
unexpected EOFs occurring during a read into a regular EOF.  It also
removes the code for SSLFileStream, to use the regular socket module's
_fileobject instead.

Version 1.12 fixes the bug in SSLSocket.accept() reported by Georg
Brandl, and adds a test case for that fix.

Version 1.13 fixes a bug in calling do_handshake() automatically
on non-blocking sockets.  Thanks to Giampaolo Rodola.  Now includes
real asyncore test case.

Version 1.14 incorporates some fixes to naming (rename "recv_from" to
"recvfrom" and "send_to" to "sendto"), and a fix to the asyncore test
case to unregister the connection handler when the connection is
closed.  It also exposes the SSL shutdown via the "unwrap" method
on an SSLSocket.  It exposes "subjectPublicKey" in the data received
from a peer cert.

Version 1.15 fixes a bug in write retries, where the output buffer has
changed location because of garbage collection during the interim.
It also provides the new flag, PROTOCOL_NOSSLv2, which selects SSL23,
but disallows actual use of SSL2.

Version 1.16 removes installing tests system-wide (which fixes the
"permission denied" error when installing in virtualenvs), adds 
``/usr/lib/i386-linux-gnu`` and ``/usr/lib/x86_64-linux-gnu`` to the
search path (which fixes compilation on ubuntu 12.04) and stopped using
``SSLv2_method`` if it's not present. Many thanks to `Denis Bilenko`_
for providing those fixes through his temporary sslfix_ fork.

The package is now maintained (bugfix only) by PyPA_.

Authorship: A cast of dozens over the years have written the Python
SSL support, including Marc-Alan Lemburg, Robin Dunn, GvR, Kalle
Svensson, Skip Montanaro, Mark Hammond, Martin von Loewis, Jeremy
Hylton, Andrew Kuchling, Georg Brandl, Bill Janssen, Chris Stawarz,
Neal Norwitz, and many others.  Thanks to Paul Moore, David Bolen and
Mark Hammond for help with the Windows side of the house.  And it's
all based on OpenSSL, which has its own cast of dozens!

.. _PyPA: https://github.com/pypa
.. _`Denis Bilenko`: https://github.com/denik
.. _`sslfix`: https://pypi.python.org/pypi/sslfix

Installation
------------

To install it, run::

  pip install ssl

or download it from https://pypi.python.org/pypi/ssl

Issues
------

Feel free to report issues at https://github.com/pypa/ssl/issues
