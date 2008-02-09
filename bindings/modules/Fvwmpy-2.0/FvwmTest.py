#! /bin/env python

"""Simple test of FVWM Python module infrastructure.

"""

__version__ = '0.1'

# sys.path munging, which will unnecessary in Python 1.4
import os
import sys
sys.path.insert(0, os.path.split(sys.argv[0])[0])

from fvwm import FvwmModule



class Test(FvwmModule):
    def unhandled_packet(self, packet):
	print 'unhandled_packet:', packet.name
	self.done = 1



if __name__ == '__main__':
    t = Test(sys.argv)
    t.mainloop()
