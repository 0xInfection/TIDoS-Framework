from __future__ import print_function

# We should have absolute imports here
from tld.utils import update_tld_names as do_update_tld_names

__title__ = 'tld.commands.update_tld_names'
__author__ = 'Artur Barseghyan'
__copyright__ = '2013-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('main',)


def main():
    """Updates TLD names.

    :example:

        python src/tld/commands/update_tld_names.py
    """

    try:
        print(do_update_tld_names())
    except Exception as err:
        print(err)


if __name__ == "__main__":
    main()
