#!/usr/bin/env python
# -*- coding: utf-8 -*-

class color(object):
  # example use:
  # print(color.red('sorry'))
  # print(color.custom('its blue', bold=True, blue=True))
    def __init__(self, text, **user_styles):

        styles = {
            # styles
            'reset': '\033[0m',
            'bold': '\033[01m',
            'disabled': '\033[02m',
            'underline': '\033[04m',
            'reverse': '\033[07m',
            'strike_through': '\033[09m',
            'invisible': '\033[08m',
            # text colors
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'orange': '\033[1;33m',
            'blue': '\033[34m',
            'purple': '\033[35m',
            'cyan': '\033[36m',
            'light_grey': '\033[37m',
            'dark_grey': '\033[90m',
            'light_red': '\033[91m',
            'light_green': '\033[92m',
            'yellow': '\033[93m',
            'light_blue': '\033[94m',
            'pink': '\033[95m',
            'light_cyan': '\033[96m',
            'white': '\033[97m',
            'default': '\033[99m',
            # background colors
            'bg_black': '\033[40m',
            'bg_red': '\033[41m',
            'bg_green': '\033[42m',
            'bg_orange': '\033[43m',
            'bg_blue': '\033[44m',
            'bg_purple': '\033[45m',
            'bg_cyan': '\033[46m',
            'bg_light_grey': '\033[47m'
        }

        self.color_text = ''
        for style in user_styles:
            try:
                self.color_text += styles[style]
            except KeyError:
                raise KeyError('def color: parameter `{}` does not exist'.format(style))

        self.color_text += text

    def __format__(self):
        return '\033[0m{}\033[0m'.format(self.color_text)

    @classmethod
    def red(clss, text):
        cls = clss(text, bold=True, red=True)
        return cls.__format__()

    @classmethod
    def blue(clss, text):
        cls = clss(text, bold=True, blue=True)
        return cls.__format__()

    @classmethod
    def yellow(clss, text):
        cls = clss(text, bold=True, yellow=True)
        return cls.__format__()

    @classmethod
    def purple(clss, text):
        cls = clss(text, bold=True, purple=True)
        return cls.__format__()

    @classmethod
    def orange(clss, text):
        cls = clss(text, bold=True, orange=True)
        return cls.__format__()

    @classmethod
    def green(clss, text):
        cls = clss(text, bold=True, green=True)
        return cls.__format__()

    @classmethod
    def white(clss, text):
        cls = clss(text, bold=True, white=True)
        return cls.__format__()

    @classmethod
    def custom(clss, text, **custom_styles):
        cls = clss(text, **custom_styles)
        return cls.__format__()
