#!/usr/bin/env python2.7

import sys

from FvwmModule import FvwmModule

class FvwmPacketMonitor(FvwmModule):
    def __init__(self, *args):
        self.__ofd = sys.stderr
        super(FvwmPacketMonitor, self).__init__(*args)
        self.registerCallback('*', self.PrintAllPackets)

    def __del__(self):
        if self.__ofd != sys.stderr:
            self.__ofd.close()

    def ParseOptionalArgs(self, *args):
        if len(args) >= 1:
            self.__ofd = open(args[0], 'w')
        self.sendFinishedStartupNotification()
        # Request a dump of configuration information
        self.send(0, "Send_ConfigInfo")

    def PrintAllPackets(self, packet):
        print >>self.__ofd, "%(syncpat)08X %(type)08X %(raw_length)08X %(time)08X:" % packet.header,
        print >>self.__ofd, type(packet)
        keys = list(packet.fields)
        #keys.sort()
        for field in keys:
            print >>self.__ofd, " %-45s ==> %20s" % (field, packet[field])
        self.__ofd.flush()


if __name__ == "__main__":
    try:
        module = FvwmPacketMonitor(*sys.argv)
        module.run()
    except KeyboardInterrupt, ex:
        pass
    print >> sys.stderr,'Clean Module Exit!'

# vim:set ts=4 sw=4 et nu:
