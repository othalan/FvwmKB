#!/usr/bin/env python2.5

import os
import socket
import sys

from pybit import BitFieldStorageLong
from pybit import BitFieldMap

def UnsignedToSigned32(value):
    value = socket.ntohl(value)
    if   value >= (1 << 32) : raise ValueError, "Value exceeds 32-bits!"
    elif value <  0         : raise ValueError, "Value is already signed!"
    if   value & (0x1 << 31): value = -value + (1 << 32)
    return value

def UnsignedToSigned16(value):
    value = socket.ntohs(value)
    if   value >= (1 << 16) : raise ValueError, "Value exceeds 16-bits!"
    elif value <  0         : raise ValueError, "Value is already signed!"
    if   value & (0x1 << 15): value = -value + (1 << 16)
    return value

def SignedToUnsigned32(value):
    if    value >= (1 << 31): raise ValueError, "Value exceeds 32-bits!"
    elif -value >  (1 << 31): raise ValueError, "Value exceeds 32-bits!"
    if    value < 0         : value = (1 << 32) + value
    return value

def SignedToUnsigned16(value):
    if    value >= (1 << 15): raise ValueError, "Value exceeds 16-bits!"
    elif -value >  (1 << 15): raise ValueError, "Value exceeds 16-bits!"
    if    value < 0         : value = (1 << 16) + value
    return value

def GetUnsigned32(value):
    value = socket.ntohl(value)
    if value < 0: value = SignedToUnsigned32(value)
    return value
def GetUnsigned16(value):
    return socket.ntohs(value)

def NullTermLongToString(value):
    chrs = []
    value >>= 8
    while value != 0:
        chrval = value % 256
        chrs.insert(0, chr(chrval))
        value >>= 8
    return ''.join(chrs)

Signed32   = "(UnsignedToSigned32,   None)"
Signed16   = "(UnsignedToSigned16,   None)"
Unsigned32 = "(GetUnsigned32,        None)"
Unsigned16 = "(GetUnsigned16,        None)"
StringVar  = "(NullTermLongToString, None)"

PacketTypes = {
   "M_NEW_PAGE": {
       'pktType': 1 << 0,
       'pktVars': {
           "vpX"   : BitFieldMap(128, 32, Signed32),
           "vpY"   : BitFieldMap(160, 32, Signed32),
           "desk"  : BitFieldMap(192, 32, Signed32),
           "width" : BitFieldMap(224, 32, Signed32),
           "height": BitFieldMap(256, 32, Signed32),
           "vpXnum": BitFieldMap(288, 32, Signed32),
           "vpYnum": BitFieldMap(320, 32, Signed32),
           }
       },
   "M_NEW_DESK": {
       'pktType': 1 << 1,
       'pktVars': {
           "desk"  : BitFieldMap(128, 32, Signed32),
           }
       },
   "M_OLD_ADD_WINDOW": {
       'pktType': 1 << 2,
       'pktVars': {
           }
       },
   "M_RAISE_WINDOW": {
       'pktType': 1 << 3,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
           }
       },
   "M_LOWER_WINDOW": {
       'pktType': 1 << 4,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
           }
       },
   "M_OLD_CONFIGURE_WINDOW": {
       'pktType': 1 << 5,
       'pktVars': {
           }
       },
   "M_FOCUS_CHANGE": {
       'pktType': 1 << 6,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "changeType"  : BitFieldMap(192, 32, Unsigned32),
           "colorHlText" : BitFieldMap(224, 32, Signed32),
           "colroHlBg"   : BitFieldMap(256, 32, Signed32),
           }
       },
   "M_DESTROY_WINDOW": {
       'pktType': 1 << 7,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
           }
       },
   "M_ICONIFY": {
       'pktType': 1 << 8,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
           "iconXPos"    : BitFieldMap(224, 32, Signed32),
           "iconYPos"    : BitFieldMap(256, 32, Signed32),
           "iconWidth"   : BitFieldMap(288, 32, Signed32),
           "iconHeight"  : BitFieldMap(320, 32, Signed32),
           "frameXPos"   : BitFieldMap(352, 32, Signed32),
           "frameYPos"   : BitFieldMap(384, 32, Signed32),
           "frameWidth"  : BitFieldMap(416, 32, Signed32),
           "frameHeight" : BitFieldMap(448, 32, Signed32),
           }
       },
   "M_DEICONIFY": {
       'pktType': 1 << 9,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
           "iconXPos"    : BitFieldMap(224, 32, Signed32),
           "iconYPos"    : BitFieldMap(256, 32, Signed32),
           "iconWidth"   : BitFieldMap(288, 32, Signed32),
           "iconHeight"  : BitFieldMap(320, 32, Signed32),
           "frameXPos"   : BitFieldMap(352, 32, Signed32),
           "frameYPos"   : BitFieldMap(384, 32, Signed32),
           "frameWidth"  : BitFieldMap(416, 32, Signed32),
           "frameHeight" : BitFieldMap(448, 32, Signed32),
           }
       },
   "M_WINDOW_NAME": {
       'pktType': 1 << 10,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
           "name"        : BitFieldMap(224, None, StringVar) # Variable Length Character String
           }
       },
   "M_ICON_NAME": {
       'pktType': 1 << 11,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
           "name"        : BitFieldMap(224, None, StringVar) # Variable Length Character String
           }
       },
   "M_RES_CLASS": {
       'pktType': 1 << 12,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
           "name"        : BitFieldMap(224, None, StringVar) # Variable Length Character String
           }
       },
   "M_RES_NAME": {
       'pktType': 1 << 13,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
           "name"        : BitFieldMap(224, None, StringVar) # Variable Length Character String
           }
       },
   "M_END_WINDOWLIST": {
       'pktType': 1 << 14,
       'pktVars': {
           # No Values
           }
       },
   "M_ICON_LOCATION": {
       'pktType': 1 << 15,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
           "xPos"        : BitFieldMap(224, 32, Signed32),
           "yPos"        : BitFieldMap(256, 32, Signed32),
           "width"       : BitFieldMap(288, 32, Signed32),
           "height"      : BitFieldMap(320, 32, Signed32),
           }
       },
   "M_MAP": {
       'pktType': 1 << 16,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
           }
       },
   "M_ERROR": {
       'pktType': 1 << 17,
       'pktVars': {
           "DUMMY_0"     : BitFieldMap(128, 32, Signed32),
           "DUMMY_1"     : BitFieldMap(160, 32, Signed32),
           "DUMMY_2"     : BitFieldMap(192, 32, Signed32),
           "error"       : BitFieldMap(224, None, StringVar) # Variable Length Character String
           }
       },
   "M_CONFIG_INFO": {
       'pktType': 1 << 18,
       'pktVars': {
           "DUMMY_0"     : BitFieldMap(128, 32, Signed32),
           "DUMMY_1"     : BitFieldMap(160, 32, Signed32),
           "DUMMY_2"     : BitFieldMap(192, 32, Signed32),
           "text"        : BitFieldMap(224, None, StringVar) # Variable Length Character String
           }
       },
   "M_END_CONFIG_INFO": {
       'pktType': 1 << 19,
       'pktVars': {
           # No Values
           }
       },
   "M_ICON_FILE": {
       'pktType': 1 << 20,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
           "name"        : BitFieldMap(224, None, StringVar) # Variable Length Character String
           }
       },
   "M_DEFAULTICON": {
       'pktType': 1 << 21,
       'pktVars': {
           "name"        : BitFieldMap(128, None, StringVar) # Variable Length Character String
           }
       },
   "M_STRING": {
       'pktType': 1 << 22,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
           "text"        : BitFieldMap(224, None, StringVar) # Variable Length Character String
           }
       },
   "M_MINI_ICON": {
       'pktType': 1 << 23,
       'pktVars': {
           # XXX This should be defined using the fvwm2 source code file
           #     libs/vpacket.h via a swig module!
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
           # The Icon
           # The Icon Filename
           }
       },
   "M_WINDOWSHADE": {
       'pktType': 1 << 24,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
           }
       },
   "M_DEWINDOWSHADE": {
       'pktType': 1 << 25,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
           }
       },
   "M_VISIBLE_NAME": {
       'pktType': 1 << 26,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
           "name"        : BitFieldMap(224, None, StringVar) # Variable Length Character String
           }
       },
    "M_SENDCONFIG": {
        'pktType': 1 << 27,
        'pktVars': {
            # Never sent by FVWM
            }
        },
    "M_RESTACK": {
        'pktType': 1 << 28,
        'pktVars': {
            # Repeating list of these three entries
            "windowId"    : BitFieldMap(128, 32, Signed32),
            "frameId"     : BitFieldMap(160, 32, Signed32),
            "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
            }
        },
   "M_ADD_WINDOW": {
       'pktType': 1 << 29,
       'pktVars': {
           }
       },
   "M_CONFIGURE_WINDOW": {
       'pktType': 1 << 30,
       'pktVars': {
           # XXX This should be defined using the fvwm2 source code file
           #     libs/vpacket.h via a swig module!
           "windowId"           : BitFieldMap(128,  32, Signed32),
           "frameId"            : BitFieldMap(160,  32, Signed32),
           "fvwmDbEntry"        : BitFieldMap(192,  32, Unsigned32), # Not Useful to us
           "frameX"             : BitFieldMap(224,  32, Signed32),
           "frameY"             : BitFieldMap(256,  32, Signed32),
           "frameWidth"         : BitFieldMap(288,  32, Unsigned32),
           "frameHeight"        : BitFieldMap(320,  32, Unsigned32),
           "desk"               : BitFieldMap(352,  32, Unsigned32),
           "layer"              : BitFieldMap(384,  32, Unsigned32),
           "hintsBaseWidth"     : BitFieldMap(416,  32, Unsigned32),
           "hintsBaseHeight"    : BitFieldMap(448,  32, Unsigned32),
           "hintsWidthInc"      : BitFieldMap(480,  32, Unsigned32),
           "hintsHeightInc"     : BitFieldMap(512,  32, Unsigned32),
           "hintsOrigWidthInc"  : BitFieldMap(544,  32, Unsigned32),
           "hintsOrigHeightInc" : BitFieldMap(576,  32, Unsigned32),
           "hintsMinWidth"      : BitFieldMap(608,  32, Unsigned32),
           "hintsMinHeight"     : BitFieldMap(640,  32, Unsigned32),
           "hintsMaxWidth"      : BitFieldMap(672,  32, Unsigned32),
           "hintsMaxHeight"     : BitFieldMap(704,  32, Unsigned32),
           "iconWindow"         : BitFieldMap(736,  32, Unsigned32),
           "iconPixmapWindow"   : BitFieldMap(768,  32, Unsigned32),
           "hintsWindowGravity" : BitFieldMap(800,  32, Unsigned32),
           "textPixel"          : BitFieldMap(832,  32, Unsigned32),
           "backPixel"          : BitFieldMap(864,  32, Unsigned32),
           "ewmhHintLayer"      : BitFieldMap(896,  32, Unsigned32),
           "ewmhHintDesktop"    : BitFieldMap(928,  32, Unsigned32),
           "ewmhWindowType"     : BitFieldMap(960,  32, Unsigned32),
           "titleHeight"        : BitFieldMap(992,  16, Unsigned16),
           "borderWidth"        : BitFieldMap(1024, 16, Unsigned16),
           "DUMMY_0"            : BitFieldMap(1088, 16, Unsigned16),
           "DUMMY_1"            : BitFieldMap(1120, 16, Unsigned16),
           }
       },
    "M_EXTENDED_MSG": {
        'pktType': 1 << 31,
        'pktVars': {
            }
        },
   "MX_VISIBLE_ICON_NAME": {
       'pktType': 1 <<  0 | 1 << 31,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32,   Signed32),
           "frameId"     : BitFieldMap(160, 32,   Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32,   Unsigned32), # Not Useful to us
           "name"        : BitFieldMap(224, None, StringVar) # Variable Length Character String
           }
       },
   "MX_ENTER_WINDOW": {
       'pktType': 1 <<  1 | 1 << 31,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
           }
       },
   "MX_LEAVE_WINDOW": {
       'pktType': 1 <<  2 | 1 << 31,
       'pktVars': {
           "windowId"    : BitFieldMap(128, 32, Signed32),
           "frameId"     : BitFieldMap(160, 32, Signed32),
           "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
           }
       },
    "MX_PROPERTY_CHANGE": {
        'pktType': 1 <<  3 | 1 << 31,
        'pktVars': {
            "type"        : BitFieldMap(128, 32, Signed32),
            "val1"        : BitFieldMap(160, 32, Signed32),
            "val2"        : BitFieldMap(192, 32, Signed32),
            "text"        : BitFieldMap(224, None, StringVar) # Variable Length Character String
            }
        },
    "MX_REPLY": {
        'pktType': 1 <<  4 | 1 << 31,
        'pktVars': {
            "windowId"    : BitFieldMap(128, 32, Signed32),
            "frameId"     : BitFieldMap(160, 32, Signed32),
            "fvwmDbEntry" : BitFieldMap(192, 32, Unsigned32), # Not Useful to us
            "text"        : BitFieldMap(224, None, StringVar) # Variable Length Character String
            }
        },
}

for name, definition in PacketTypes.items():
    definition['name'] = name
    PacketTypes[definition['pktType']] = definition

def _GetLength(length): return GetUnsigned32(length) * 4

class FvwmModuleException(Exception): pass
class FvwmPacketException(FvwmModuleException): pass
class FvwmPacketIdException(FvwmPacketException): pass

class FvwmPacket(object):
    __metaclass__ = BitFieldStorageLong
    syncpat       =  BitFieldMap(0,   32, (GetUnsigned32, None))
    packetType    =  BitFieldMap(32,  32, (GetUnsigned32, None))
    length        =  BitFieldMap(64,  32, (_GetLength,    None))
    time          =  BitFieldMap(96,  32, (GetUnsigned32, None))
    packetData    =  BitFieldMap(128, None)
    headerBytes   =  16
    pktClasses    =  {}

    varForm       = """    %(name)-13s= BitFieldMap(%(offset)i, %(length)s, %(conversion)s)\n"""

    classForm     = """
global FvwmPacket_%(name)s
class FvwmPacket_%(name)s(FvwmPacket):
    __metaclass__ = BitFieldStorageLong
    __name        = "%(name)s"
    __type        = %(type)i
    __fieldNames  = %(fields)s
    packetName    = property(lambda self: self.__name,       None, "Packet Name")
    expectedType  = property(lambda self: self.__type,       None, "Packet Expected Type Code")
    fields        = property(lambda self: self.__fieldNames, None, "Packet Data Field Names")
%(body)s
cls.pktClasses["%(name)s"] = FvwmPacket_%(name)s
cls.pktClasses[%(type)i]   = FvwmPacket_%(name)s
"""

    @classmethod
    def GetClass(cls, toGet):
        if not toGet in cls.pktClasses:
            try:
                toGet = int(toGet)
            except ValueError:
                pass

            try:
                definition = PacketTypes[toGet]
            except KeyError:
                raise FvwmPacketIdException, "Invalid ID Requested: '%X'" % toGet

            cls.CreateClass(**definition)
        return cls.pktClasses[toGet]

    @classmethod
    def CreateClass(cls, name, pktType, pktVars):
        data = {
            "name"  : name,
            'type'  : pktType,
            "body"  : "",
            "fields": [],
            }
        for name, value in pktVars.iteritems():
            data['body'] += cls.varForm % {
                'name'      : name,
                'offset'    : value.start,
                'length'    : value.bits,
                'conversion': value.convert,
                }
            data['fields'].append(name)
        newClass = cls.classForm % data
        exec newClass


class FvwmModule(object):
    moduleName     = property(lambda self: self.__moduleName    , None)
    fdSend         = property(lambda self: self.__fdSend        , None)
    fdRecv         = property(lambda self: self.__fdRecv        , None)
    configFile     = property(lambda self: self.__configFile    , None)
    conextWindowId = property(lambda self: self.__conextWindowId, None)
    launchContext  = property(lambda self: self.__launchContext , None)

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

        self.ParseOptionalArgs(*args)

        self.__PacketMonitor()

    def ParseOptionalArgs(self, *args):
        """Override this function to parse optional command-line arguments"""
        pass

    def __PacketMonitor(self):
        while not self.__exit:
            packet = FvwmPacket()
            packetHeader  = self.fdRecv.read(packet.headerBytes)
            packet.value  = packetHeader
            packetData    = self.fdRecv.read(packet.length - packet.headerBytes)
            packetClass   = packet.GetClass(packet.packetType)
            pkt           = packetClass()
            pkt.value     = packetHeader + packetData
            for (packetName, cbFunc) in self.__cbRegistry:
                if packetName == pkt.packetName or packetName == '*':
                    cbFunc(pkt)

    def RegisterCallback(self, packetName, cbFunc):
        try:
            self.__cbRegistry.append((packetName, cbFunc))
        except AttributeError:
            self.__cbRegistry = [(packetName, cbFunc)]

    def ExitApp(self):
        self.__exit = True

    def __del__(self):
        self.fdSend.close()
        self.fdRecv.close()

if __name__ == "__main__":
    module = FvwmModule(*sys.argv)

# vim:set ts=4 sw=4 et nu:
