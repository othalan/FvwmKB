#! /usr/bin/env python

"""A simple example use of Fvwm.py for FVWM version 2.

Requires Fvwm 2.x.  You cannot run this from the command line; it must be
forked by Fvwm.  See the Fvwm documentation for details.

Copyright 1996-2001 Barry A. Warsaw <bwarsaw@python.org>

"""
__version__ = '1.1'

import os
import sys
from Fvwm import FvwmModule



def error(msg, exit=0):
    print '[Snap] <<ERROR>>', msg
    if exit:
	sys.exit(exit)

if __name__ == '__main__':
    # create the module to interface with Fvwm
    m = FvwmModule(sys.argv)
    # read configuration lines.  We're only looking for those that
    # start with `*Snap'
    snappers = {}
    for config in m.get_configinfo().get_infolines('Snap'):
	try:
	    [ignore, snapper, x, y, w, h] = config.split()
	    snappers[snapper] = [x, y, w, h]
	except ValueError:
	    error('Ignoring badly formed line: %s' % config)
    # now figure out where you want to snap to
    snapto = m.args[0]
    try:
	[x, y, w, h] = snappers[snapto]
	window = int(m.appcontext, 16)
    except KeyError:
	error("Don't know how to snap to: %s" % snapto, -1)
    except ValueError:
	error("Whoa Nelly!  Can't get a window number: %s" % m.appcontext, -2)
    # do the snapping
    m.send('Move %s %s' % (x, y), window, cont=1)
    m.send('Resize %s %s' % (w, h), window, cont=1)
    m.send('Focus', window, cont=0)
