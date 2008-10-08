#!/usr/bin/env python2.5

from fvwm import FvwmModule
from fvwm import FvwmPacket

class FvwmBgRotator(FvwmModule):
    def __init__(self, *args):
        super(FvwmBgRotator, self).__init__(*args)
    def ConfigInfo(self, packet): pass

# vim:set ts=4 sw=4 et nu:
