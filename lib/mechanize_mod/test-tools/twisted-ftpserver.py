import optparse
import sys

import twisted.cred.checkers
import twisted.cred.credentials
import twisted.cred.portal
import twisted.internet
import twisted.protocols.ftp
from twisted.python import filepath, log

from zope.interface import implements


def make_ftp_shell(avatar_id, root_path):
    if avatar_id is twisted.cred.checkers.ANONYMOUS:
        return twisted.protocols.ftp.FTPAnonymousShell(root_path)
    else:
        return twisted.protocols.ftp.FTPShell(root_path)


class FTPRealm(object):

    implements(twisted.cred.portal.IRealm)

    def __init__(self, root_path):
        self._root_path = filepath.FilePath(root_path)

    def requestAvatar(self, avatarId, mind, *interfaces):
        for iface in interfaces:
            if iface is twisted.protocols.ftp.IFTPShell:
                avatar = make_ftp_shell(avatarId, self._root_path)
                return (twisted.protocols.ftp.IFTPShell,
                        avatar,
                        getattr(avatar, "logout", lambda: None))
        raise NotImplementedError()


class FtpServerFactory(object):
    """
    port = FtpServerFactory("/tmp", 2121).makeListner()
    self.addCleanup(port.stopListening)
    """

    def __init__(self, root_path, port):
        factory = twisted.protocols.ftp.FTPFactory()
        realm = FTPRealm(root_path)
        portal = twisted.cred.portal.Portal(realm)
        portal.registerChecker(twisted.cred.checkers.AllowAnonymousAccess(),
                               twisted.cred.credentials.IAnonymous)
        checker = twisted.cred.checkers.\
            InMemoryUsernamePasswordDatabaseDontUse()
        checker.addUser("john", "john")
        portal.registerChecker(checker)
        factory.tld = root_path
        factory.userAnonymous = "anon"
        factory.portal = portal
        factory.protocol = twisted.protocols.ftp.FTP
        self._factory = factory
        self._port = port

    def makeListener(self):
        # XXX use 0 instead of self._port?
        return twisted.internet.reactor.listenTCP(
            self._port, self._factory, interface="127.0.0.1")


def parse_options(args):
    parser = optparse.OptionParser()
    parser.add_option("--log", action="store_true")
    parser.add_option("--port", type="int", default=2121)
    options, remaining_args = parser.parse_args(args)
    options.root_path = remaining_args[0]
    return options


def main(argv):
    options = parse_options(argv[1:])
    if options.log:
        log.startLogging(sys.stdout)
    factory = FtpServerFactory(options.root_path, options.port)
    factory.makeListener()
    twisted.internet.reactor.run()


if __name__ == "__main__":
    main(sys.argv)
