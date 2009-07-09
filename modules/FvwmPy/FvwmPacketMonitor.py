#!/usr/bin/env python2.5

import sys

from fvwm import FvwmModule
from fvwm import FvwmPacket

class FvwmPacketMonitor(FvwmModule):
    def __init__(self, *args):
        self.registerCallback('*', self.PrintAllPackets)
        self.__ofd = sys.stderr
        super(FvwmPacketMonitor, self).__init__(*args)

    def ParseOptionalArgs(self, *args):
        if len(args) >= 1:
            self.__ofd = open(args[0], 'w')
        self.sendFinishedStartupNotification()
        # Request a dump of configuration information
        #self.send(0, "Send_ConfigInfo")

    def PrintAllPackets(self, packet):
        print >>self.__ofd, "%(syncpat)08X %(packetType)08X %(_raw_length)08X %(time)08X:" % packet,
        print >>self.__ofd, type(packet)
        keys = list(packet.fields)
        keys.sort()
        for field in keys:
            try:
                print >>self.__ofd, " %-20s ==> %20s" % (field, packet[field])
            except Exception, ex:
                if packet.pktType != FvwmPacket.TYPE_C_STRUCT:
                    self.__ofd.write('ERROR: %s ==> %s: %s\n' % (field, packet["_raw_%s" % field], ex))
                    self.__ofd.flush()
                    raise
                else:
                    self.__ofd.write('ERROR: %s ==> %s: %s\n' % (field, packet[field], ex))
                    self.__ofd.flush()
                    raise
        self.__ofd.flush()


if __name__ == "__main__":
    try:
        module = FvwmPacketMonitor(*sys.argv)
    except KeyboardInterrupt, ex:
        pass

# vim:set ts=4 sw=4 et nu:
