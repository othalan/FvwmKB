#! /bin/env python

"""FvwmWinList implemented in Python."""

__version__ = '0.1'


import os
import sys
# path hackage, unnecessary in Python 1.4
sys.path.insert(0, os.path.split(sys.argv[0])[0])

from Fvwm import FvwmModule

def printinfo(info):
    for i in info:
	print "`%s'" % i



class WinList(FvwmModule):
    def __init__(self):
	FvwmModule.__init__(self, sys.argv)
	info = self.get_configinfo()
	print 'IconPath   ==', info.get_iconpath()
	print 'PixmapPath ==', info.get_pixmappath()
	print 'ClickTime  ==', info.get_clicktime()
	print '1 =========='
	for line in info.get_infolines():
	    print line
	print '2 =========='
	for line in info.get_infolines('FvwmIdent'):
	    print line


if __name__ == '__main__':
    w = WinList()
