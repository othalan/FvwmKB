#!/usr/bin/env python2.5

import sys

from fvwm import FvwmModule
from fvwm import FvwmPacket

class FvwmPacketMonitor(FvwmModule):
    def __init__(self, *args):
        self.RegisterCallback('*', self.PrintAllPackets)
        super(FvwmPacketMonitor, self).__init__(*args)

    def PrintAllPackets(self, packet):
        print "%(syncpat)08X %(packetType)08X %(_raw_length)08X %(time)08X:" % packet,
        print type(packet)
        for field in packet.fields:
            print " %20s ==> %20s" % (field, packet[field])


if __name__ == "__main__":
    try:
        module = FvwmPacketMonitor(*sys.argv)
    except KeyboardInterrupt, ex:
        pass

# vim:set ts=4 sw=4 et nu:
