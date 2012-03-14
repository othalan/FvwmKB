################################################################################
# FVWM to Module Interface

import FvwmPkt
import os
import sys
import struct

################################################################################
class ByteSequence(object):
    __doc__ = """
This class uses the 'struct' library to provide a means of easy conversion
between numeric values and a string containing equivalent bytes for binary
data transfers.
"""

    __StructIntSizes = {
        struct.calcsize('c'): 'c',
        struct.calcsize('b'): 'b',
        struct.calcsize('h'): 'h',
        struct.calcsize('i'): 'i',
        struct.calcsize('l'): 'l',
        struct.calcsize('q'): 'q',
        }
    __StructFloatSizes = {
        struct.calcsize('f'): 'f',
        struct.calcsize('d'): 'd',
        }

    def __init__(self, value, bytes=0, endian='@'):
        if endian not in '@=<>!':
            raise ValueError("Invalid Endian Definition: %s" % endian)
        else:
            self.__endian = endian

        if isinstance(value, str):
            self.__value  = value
            self.__bytes  = len(value)
        elif isinstance(value, int) and bytes in list(self.__StructIntSizes.keys()):
            if value < 0:
                code = self.__StructIntSizes[bytes]
            else:
                code = self.__StructIntSizes[bytes].upper()
            self.__value = struct.pack("%s%s" % (self.__endian, code), value)
            self.__bytes = len(self.__value)
        elif isinstance(value, float) and bytes in list(self.__StructFloatSizes.keys()):
            code = self.__StructFloatSizes[bytes].upper()
            self.__value = struct.pack("%s%s" % (self.__endian, code), value)
            self.__bytes = len(self.__value)
        else:
            raise ValueError("Invalid C data type byte size specified: %i" % bytes)

    def __str__(self):
        return self.__value
    def __float__(self):
        try:
            return struct.unpack("%s%s" % (self.__endian,
                                           self.__StructFloatSizes[self.__bytes]),
                                 self.__value)[0]
        except KeyError:
            raise ValueError("Invalid Float Byte Size: %i" % self.__bytes)
    def __int__(self):
        try:
            return struct.unpack("%s%s" % (self.__endian,
                                           self.__StructIntSizes[self.__bytes]),
                                 self.__value)[0]
        except KeyError:
            raise ValueError("Invalid Integer Byte Size: %i" % self.__bytes)

    def str(self)  : return self.__value
    def int(self)  : return int(self)
    def float(self): return float(self)

################################################################################

class FvwmModule(object):
    __doc__ = """
This class provides the communication between an FVWM session and a Python
module.  It is designed to be used as the command-line interface entry point
in a file, typically with the following usage:

    class MyModule(FvwmModule)
        # ... setup the module here ...

    module = MyModule(*sys.argv)
    module.run()

This class provides the following functionality for subclasses implementing
a module:

- Register callback functions for text commands (self.registerCommand)
- Register callback functions for packet types  (self.registerCallback)
- Send data and Commands to FVWM                (self.send*)

Implementation of a new module typically will involve implementing the content
of these methods:

    __init__        Module Initialization -- Setup callbacks here
    parseOptArgs    Parse optional command-line arguments -- FVWM NOT available!
    setup           Module Setup Code -- Initialization with FVWM
"""

    ################################################################################
    # Properties
    moduleName     = property(lambda self: self.__moduleName    , None, None, "Module name from FVWM")
    fdSend         = property(lambda self: self.__fdSend        , None, None, "Send file descriptor")
    fdRecv         = property(lambda self: self.__fdRecv        , None, None, "Receive file descriptor")
    configFile     = property(lambda self: self.__configFile    , None, None, "FVWM Configuration File")
    conextWindowId = property(lambda self: self.__conextWindowId, None, None, "FVWM Context Window ID")
    launchContext  = property(lambda self: self.__launchContext , None, None, "FVWM Launch Context")

    def Usage(self, exit=False):
        print "Usage: %s fdSend fdRecv configFile contextWinId launchContext [options]" % self.moduleName
        if exit: sys.exit(-1)

    def __init__(self,
            name           = None,
            fdSend         = None,
            fdRecv         = None,
            configFile     = None,
            conextWindowId = None,
            launchContext  = None,
            *args):
        self.__moduleName     = name or "<invalid>"

        if name           == None: self.Usage(True)
        if fdSend         == None: self.Usage(True)
        if fdRecv         == None: self.Usage(True)
        if configFile     == None: self.Usage(True)
        if conextWindowId == None: self.Usage(True)
        if launchContext  == None: self.Usage(True)

        try:
            try:
                self.__fdSend = os.fdopen(int(fdSend), 'wb', 0)
            except ValueError, ex:
                self.__fdSend = open(fdSend, 'wb', 0)
            try:
                self.__fdRecv = os.fdopen(int(fdRecv), 'rb', 0)
            except ValueError, ex:
                self.__fdRecv = open(fdRecv, 'rb', 0)
        except IOError, ex:
            self.Usage(True)

        self.__configFile     = configFile
        self.__conextWindowId = conextWindowId
        self.__launchContext  = launchContext
        self.__exit           = False

        self.registerCallback('M_STRING', self.onString)
        self.registerCommand('NOP', self.onNop)

        self.ParseOptionalArgs(*args)

    # XXX Is the setup function necessary? Should there be pre-registered callback? XXX
    def setup(self):
        """Override this function for user setup which should occur after FVWM is connected!"""
        pass

    def run(self):
        self.setup()
        self.__PacketMonitor()

    def parseOptArgs(self, *args):
        """Override this function to parse optional command-line arguments"""
        pass

    def __PacketMonitor(self):
        while not self.__exit:
            packetHeader = FvwmPkt.FvwmPktHeader()
            packetData  = ''
            while len(packetData) < len(packetHeader):
                received = self.fdRecv.read(len(packetHeader) - len(packetData))
                print 'bar', repr(received)
                if len(received) > 0:
                    packetData += received
                else:
                    # We have been closed down, so exit the packet monitor
                    return
            packetHeader.data = packetData
            packetData        = ''
            while len(packetData) < packetHeader.length:
                received = self.fdRecv.read(packetHeader.length - len(packetData))
                if len(received) > 0:
                    packetData += received
                else:
                    # We have been closed down, so exit the packet monitor
                    return

            pkt      = FvwmPkt.getFvwmPktObj(packetHeader.type,
                                             packetHeader.length)

            if pkt.type == FvwmPkt.PKT_TYPE_SWIG:
                pass
                #pkt.cPktSet(packetData)
            else:
                pkt.data = packetHeader.data + packetData

            for (packetName, cbFunc) in self.__cbRegistry:
                if packetName == pkt.name or packetName == '*':
                    cbFunc(pkt)

    def send(self, window, message, exit=False):
        try:
            print "SEND TO [%X]: %s" % (window, message)
            win=ByteSequence(window, 4)
            length=ByteSequence(len(message), 4)
            doexit=ByteSequence(0 if exit else 1, 4)
            self.fdSend.write("%s%s%s%s" % (win,
                                            length,
                                            message,
                                            doexit))
        except AttributeError, ex:
            raise
            raise AttributeError, "Send [%X:%s] failed: %s" % (window, message, ex)

    def sendTo(self, window, message, exit=False):
        self.send(window, "WindowId %i %s" % (window, message), exit)

    def sendFinishedStartupNotification(self):
        self.send(0, "NOP FINISHED STARTUP")

    def sendUnlockNotification(self):
        self.send(0, "NOP UNLOCK")

    def sendQuitNotification(self):
        self.send(0, "NOP UNLOCK", True)
        self.exitApp()

    def setMessageMask(self, mask):
        """Set the message types to receive"""
        self.send(0, "SET_MASK %i" % mask)

    def setSyncMask(self, mask):
        self.send(0, "SET_SYNC_MASK %I" % MASK)

    def setNoGrabMask(self, mask):
        self.send(0, "SET_NOGRAB_MASK %I" % MASK)

    def initGetConfigLine(self, match):
        """Send only configuration lines which match this string (e.g. "*FooModule")"""
        self.send(0, "Send_ConfigInfo %s" % match)

    def onString(self, packet):
        cmd = packet.text.split()
        for (cmdName, cbFunc) in self.__cmdRegistry:
            if cmdName == cmd[0] or cmdName == '*':
                cbFunc(*cmd)

    def onNop(self, *args):
        pass

    def registerCallback(self, packetName, cbFunc):
        try:
            self.__cbRegistry.append((packetName, cbFunc))
        except AttributeError:
            self.__cbRegistry = [(packetName, cbFunc)]

    def unregisterCallback(self, packetName, cbFunc):
        try:
            self.__cbRegistry.remove((packetName, cbFunc))
        except ValueError:
            print >>sys.stderr, "WARNING: Callback (%s,%s) not found, thus not removed" % (packetName, cbFunc)

    def registerCommand(self, cmdName, cbFunc):
        try:
            self.__cmdRegistry.append((cmdName, cbFunc))
        except AttributeError:
            self.__cmdRegistry = [(cmdName, cbFunc)]

    def unregisterCommand(self, cmdName, cbFunc):
        try:
            self.__cmdRegistry.remove((cmdName, cbFunc))
        except ValueError:
            print >>sys.stderr, "WARNING: Command (%s,%s) not found, thus not removed" % (cmdName, cbFunc)

    def exitApp(self):
        self.__exit = True

    def __del__(self):
        self.fdSend.close()
        self.fdRecv.close()

# vim:set tw=180 ts=4 sw=4 et nu:
