from ..base import BaseTLDSource

__title__ = 'tld.sources.mozilla'
__author__ = 'Artur Barseghyan'
__copyright__ = '2013-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('MozillaTLDSource',)


class MozillaTLDSource(BaseTLDSource):
    """Mozilla TLD source."""

    uid = 'mozilla'
