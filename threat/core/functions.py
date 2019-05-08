#!/usr/bin/env python
from modules.recon.recon import recon
from modules.enumeration.scanenum import scanenum
from modules.exploitation.exploitation import exploitation
from modules.vulnysis.vulnysis import vulnysis
from modules.recon.passive_recon import passive_recon
from modules.recon.dig import dig

functions = {
    'recon':recon,
    'scanenum':scanenum,
    'exploitation':exploitation,
    'vulnysis':vulnysis,
    #'post':post

    # recon related
    'passive_recon':passive_recon,
    #'active_recon':active_recon,
    #'infodisc':infodisc,

    'dig':dig,
    #''
}