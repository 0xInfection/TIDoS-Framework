#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_____, ___
   '+ .;    
    , ;   
     .   
           
       .    
     .;.    
     .;  
      :  
      ,   
       

┌─[TIDoS]─[]
└──╼ VainlyStrain
"""

import argparse
import sys
from core.methods.print import banner
from core.Core.colors import color, RB, C, RC, R, RD

class VaileParser(argparse.ArgumentParser):
    def error(self, message):
        banner()
        self.print_usage(sys.stderr)
        self.exit(2, '{}[-]\033[0m\033[1m Invalid/missing params\033[0m\n{}[HINT]\033[0m\033[0m {}\n'.format(R, R, message))
    def print_help(self):
        print('''{}Vsynta.:{} {}tidos{} [-v VIC] [-p] [-a CA] [-s] 
          [-f] [-l M] [-h] [-c VAL]
        [--app] [-q]

  -v VIC, --victim VIC  {}Target to attack per cli{}
  -l M, --load M        {}Module to load per cli{}
  -a CA, --list CA      {}List modules of CA{}
  -p, --tor             {}Pipe Attacks thro. Tor?{}
  -s, --session         {}Is VIC a session file?{}
  -q, --quiet           {}Start Console quietly{}
  -f, --fetch           {}Check for & install updates{}
  -c, --file            {}Automation using VAL file{}
  --app                 {}Run TIDoS graphical interface{}'''.format(RC, color.END, RB, color.END, RC, color.END, RC, color.END, RC, color.END, RC, color.END, RC, color.END, RC, color.END, RC, color.END, RC, color.END, RC, color.END))

class VaileFormatter(argparse.RawDescriptionHelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = RD + 'Vsynta ' + color.END
            return super(VaileFormatter, self).add_usage("{}tidos{} [-v VIC] [-p] [-a CA] [-s]\n          [-f] [-l M] [-h] [-c VAL]\n        [--app] [-q]".format(RB,color.END), actions, groups, prefix)

def build_parser():
    p = VaileParser(formatter_class=VaileFormatter, add_help=False)
    p.add_argument('-v', '--victim',
                   help='Target to attack (without loading entire framework)',
                   metavar='VIC'
                   )
    p.add_argument('-l', '--load',
                   help='Module to use (without loading entire framework)',
                   metavar='M'
                   )
    p.add_argument('-h', '--help',
                   help="Display this help message and exit",
                   action="store_true"
                   )
    p.add_argument('-s', '--session',
                   help="Is --victim a session file?",
                   action="store_true"
                   )
    p.add_argument('-p', '--tor',
                   help="Pipe Attacks through Tor?",
                   action="store_true"
                   )
    p.add_argument('-a', '--list',
                   help='List modules of category CA',
                   metavar='CA'
                   )
    p.add_argument('-q', '--quiet',
                   help='Start Console quietly',
                   action='store_true'
                   )
    p.add_argument('-f', '--fetch',
                   help='Check for and install updates.',
                   action='store_true'
                   )
    p.add_argument('-c', '--file',
                   help='Automation using VAL file',
                   metavar='VAL'
                   )
    #p.epilog = "Beware, my friend. These are dark times."
    return p
