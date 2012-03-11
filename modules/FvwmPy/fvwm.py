#!/usr/bin/env python2.7

import os
import socket
import struct
import sys

import FvwmPkt

from pybit import ByteMap
from pybit import ByteMapMeta
from pybit import uint
from pybit import ulong
from pybit import ByteSequence

def UnsignedToSigned32(value):
    value = socket.ntohl(value)
    if   value >= (1 << 32) : raise ValueError, "Value exceeds 32-bits: %s" % value
    elif value <  0         : raise ValueError, "Value is already signed: %s" % value
    if   value & (0x1 << 31): value = -value + (1 << 32)
    return value

def UnsignedToSigned16(value):
    value = socket.ntohs(value)
    if   value >= (1 << 16) : raise ValueError, "Value exceeds 16-bits: %s" % value
    elif value <  0         : raise ValueError, "Value is already signed: %s" % value
    if   value & (0x1 << 15): value = -value + (1 << 16)
    return value

def SignedToUnsigned32(value):
    if    value >= (1 << 31): raise ValueError, "Value exceeds 32-bits: %s" % value
    elif -value >  (1 << 31): raise ValueError, "Value exceeds 32-bits: %s" % value
    if    value < 0         : value = (1 << 32) + value
    return value

def SignedToUnsigned16(value):
    if    value >= (1 << 15): raise ValueError, "Value exceeds 16-bits: %s" % value
    elif -value >  (1 << 15): raise ValueError, "Value exceeds 16-bits: %s" % value
    if    value < 0         : value = (1 << 16) + value
    return value

def GetUnsigned32(value):
    value = socket.ntohl(value)
    if value < 0: value = SignedToUnsigned32(value)
    return value
def GetUnsigned16(value):
    return socket.ntohs(value)

def NullTermLongToString(value):
    value = str(value).rstrip('\0').strip()
    return value

Signed32   = "(UnsignedToSigned32,   None)"
Signed16   = "(UnsignedToSigned16,   None)"
Unsigned32 = "(GetUnsigned32,        None)"
Unsigned16 = "(GetUnsigned16,        None)"
StringVar  = "(NullTermLongToString, None)"

PacketTypes = {
   "M_NEW_PAGE": {
       'pktType': 1 << 0,
       'pktVars': {
           "vpX"   : ByteMap(16, 4, 'int'),
           "vpY"   : ByteMap(20, 4, 'int'),
           "desk"  : ByteMap(24, 4, 'int'),
           "width" : ByteMap(28, 4, 'int'),
           "height": ByteMap(32, 4, 'int'),
           "vpXnum": ByteMap(36, 4, 'int'),
           "vpYnum": ByteMap(40, 4, 'int'),
           }
       },
   "M_NEW_DESK": {
       'pktType': 1 << 1,
       'pktVars': {
           "desk"  : ByteMap(16, 4, 'int'),
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
           "windowId"    : ByteMap(16, 4, 'ulong'),
           "frameId"     : ByteMap(20, 4, 'int'),
           "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
           }
       },
   "M_LOWER_WINDOW": {
       'pktType': 1 << 4,
       'pktVars': {
           "windowId"    : ByteMap(16, 4, 'ulong'),
           "frameId"     : ByteMap(20, 4, 'int'),
           "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
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
           "windowId"    : ByteMap(16, 4, 'ulong'),
           "frameId"     : ByteMap(20, 4, 'int'),
           "changeType"  : ByteMap(24, 4, 'ulong'),
           "colorHlText" : ByteMap(28, 4, 'int'),
           "colorHlBg"   : ByteMap(32, 4, 'int'),
           }
       },
   "M_DESTROY_WINDOW": {
       'pktType': 1 << 7,
       'pktVars': {
           "windowId"    : ByteMap(16, 4, 'ulong'),
           "frameId"     : ByteMap(20, 4, 'int'),
           "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
           }
       },
   "M_ICONIFY": {
       'pktType': 1 << 8,
       'pktVars': {
           "windowId"    : ByteMap(16, 4, 'ulong'),
           "frameId"     : ByteMap(20, 4, 'int'),
           "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
           "iconXPos"    : ByteMap(28, 4, 'int'),
           "iconYPos"    : ByteMap(32, 4, 'int'),
           "iconWidth"   : ByteMap(36, 4, 'int'),
           "iconHeight"  : ByteMap(40, 4, 'int'),
           "frameXPos"   : ByteMap(44, 4, 'int'),
           "frameYPos"   : ByteMap(48, 4, 'int'),
           "frameWidth"  : ByteMap(52, 4, 'int'),
           "frameHeight" : ByteMap(56, 4, 'int'),
           }
       },
   "M_DEICONIFY": {
       'pktType': 1 << 9,
       'pktVars': {
           "windowId"    : ByteMap(16, 4, 'ulong'),
           "frameId"     : ByteMap(20, 4, 'int'),
           "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
           "iconXPos"    : ByteMap(28, 4, 'int'),
           "iconYPos"    : ByteMap(32, 4, 'int'),
           "iconWidth"   : ByteMap(36, 4, 'int'),
           "iconHeight"  : ByteMap(40, 4, 'int'),
           "frameXPos"   : ByteMap(44, 4, 'int'),
           "frameYPos"   : ByteMap(48, 4, 'int'),
           "frameWidth"  : ByteMap(52, 4, 'int'),
           "frameHeight" : ByteMap(56, 4, 'int'),
           }
       },
   "M_WINDOW_NAME": {
       'pktType': 1 << 10,
       'pktVars': {
           "windowId"    : ByteMap(16, 4, 'ulong'),
           "frameId"     : ByteMap(20, 4, 'int'),
           "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
           "name"        : ByteMap(28, None, StringVar) # Variable Length Character String
           }
       },
   "M_ICON_NAME": {
       'pktType': 1 << 11,
       'pktVars': {
           "windowId"    : ByteMap(16, 4, 'ulong'),
           "frameId"     : ByteMap(20, 4, 'int'),
           "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
           "name"        : ByteMap(28, None, StringVar) # Variable Length Character String
           }
       },
   "M_RES_CLASS": {
       'pktType': 1 << 12,
       'pktVars': {
           "windowId"    : ByteMap(16, 4, 'ulong'),
           "frameId"     : ByteMap(20, 4, 'int'),
           "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
           "name"        : ByteMap(28, None, StringVar) # Variable Length Character String
           }
       },
   "M_RES_NAME": {
       'pktType': 1 << 13,
       'pktVars': {
           "windowId"    : ByteMap(16, 4, 'ulong'),
           "frameId"     : ByteMap(20, 4, 'int'),
           "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
           "name"        : ByteMap(28, None, StringVar) # Variable Length Character String
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
           "windowId"    : ByteMap(16, 4, 'ulong'),
           "frameId"     : ByteMap(20, 4, 'int'),
           "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
           "xPos"        : ByteMap(28, 4, 'int'),
           "yPos"        : ByteMap(32, 4, 'int'),
           "width"       : ByteMap(36, 4, 'int'),
           "height"      : ByteMap(40, 4, 'int'),
           }
       },
   "M_MAP": {
       'pktType': 1 << 16,
       'pktVars': {
           "windowId"    : ByteMap(16, 4, 'ulong'),
           "frameId"     : ByteMap(20, 4, 'int'),
           "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
           }
       },
   "M_ERROR": {
       'pktType': 1 << 17,
       'pktVars': {
           "DUMMY_0"     : ByteMap(16, 4, 'int'),
           "DUMMY_1"     : ByteMap(20, 4, 'int'),
           "DUMMY_2"     : ByteMap(24, 4, 'int'),
           "error"       : ByteMap(28, None, StringVar) # Variable Length Character String
           }
       },
   "M_CONFIG_INFO": {
       'pktType': 1 << 18,
       'pktVars': {
           "DUMMY_0"     : ByteMap(16, 4, 'int'),
           "DUMMY_1"     : ByteMap(20, 4, 'int'),
           "DUMMY_2"     : ByteMap(24, 4, 'int'),
           "text"        : ByteMap(28, None, StringVar) # Variable Length Character String
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
           "windowId"    : ByteMap(16, 4, 'ulong'),
           "frameId"     : ByteMap(20, 4, 'int'),
           "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
           "name"        : ByteMap(28, None, StringVar) # Variable Length Character String
           }
       },
   "M_DEFAULTICON": {
       'pktType': 1 << 21,
       'pktVars': {
           "name"        : ByteMap(16, None, StringVar) # Variable Length Character String
           }
       },
   "M_STRING": {
       'pktType': 1 << 22,
       'pktVars': {
           "windowId"    : ByteMap(16, 4, 'ulong'),
           "frameId"     : ByteMap(20, 4, 'int'),
           "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
           "text"        : ByteMap(28, None, StringVar) # Variable Length Character String
           }
       },
   "M_MINI_ICON": {
       'pktType': 1 << 23,
       'pktUnion' : 'FvwmPkt.MiniIconPacketUnion',
       'pktStruct': 'FvwmPkt.MiniIconPacket',
       'pktSize'  : 'FvwmPkt.MiniIconPacketSize',
       'pktStart' : 16,
       'pktVars'  : {
           # Rename some packet fields for consistency and clarity
           "windowId"   : 'w',
           "frameId"    : 'frame',
           "fvwmDbEntry": 'fvwmwin',

          ## XXX This should be defined using the fvwm2 source code file
          ##     libs/vpacket.h via a swig module!
          #"windowId"    : ByteMap(16, 4, 'ulong'),
          #"frameId"     : ByteMap(20, 4, 'int'),
          #"fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
           # The Icon
           # The Icon Filename
           }
       },
   "M_WINDOWSHADE": {
       'pktType': 1 << 24,
       'pktVars': {
           "windowId"    : ByteMap(16, 4, 'ulong'),
           "frameId"     : ByteMap(20, 4, 'int'),
           "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
           }
       },
   "M_DEWINDOWSHADE": {
       'pktType': 1 << 25,
       'pktVars': {
           "windowId"    : ByteMap(16, 4, 'ulong'),
           "frameId"     : ByteMap(20, 4, 'int'),
           "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
           }
       },
   "M_VISIBLE_NAME": {
       'pktType': 1 << 26,
       'pktVars': {
           "windowId"    : ByteMap(16, 4, 'ulong'),
           "frameId"     : ByteMap(20, 4, 'int'),
           "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
           "name"        : ByteMap(28, None, StringVar) # Variable Length Character String
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
            "windowId"    : ByteMap(16, 4, 'ulong'),
            "frameId"     : ByteMap(20, 4, 'int'),
            "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
            }
        },
   "M_ADD_WINDOW": {
       'pktType': 1 << 29,
       'pktUnion' : 'FvwmPkt.ConfigWinPacketUnion',
       'pktStruct': 'FvwmPkt.ConfigWinPacket',
       'pktSize'  : 'FvwmPkt.ConfigWinPacketSize',
       'pktStart' : 16,
       'pktVars'  : {
           # Rename some packet fields for consistency and clarity
           "windowId"   : 'w',
           "frameId"    : 'frame',
           "fvwmDbEntry": 'fvwmwin',
      #'pktVars': {
      #    # XXX This should be defined using the fvwm2 source code file
      #    #     libs/vpacket.h via a swig module!
      #    "windowId"           : ByteMap(16,   4, 'ulong'),
      #    "frameId"            : ByteMap(20,   4, 'int'),
      #    "fvwmDbEntry"        : ByteMap(24,   4, 'ulong'), # Not Useful to us
      #    "frameX"             : ByteMap(28,   4, 'int'),
      #    "frameY"             : ByteMap(32,   4, 'int'),
      #    "frameWidth"         : ByteMap(36,   4, 'ulong'),
      #    "frameHeight"        : ByteMap(40,   4, 'ulong'),
      #    "desk"               : ByteMap(44,   4, 'ulong'),
      #    "layer"              : ByteMap(48,   4, 'ulong'),
      #    "hintsBaseWidth"     : ByteMap(52,   4, 'ulong'),
      #    "hintsBaseHeight"    : ByteMap(56,   4, 'ulong'),
      #    "hintsWidthInc"      : ByteMap(60,   4, 'ulong'),
      #    "hintsHeightInc"     : ByteMap(64,   4, 'ulong'),
      #    "hintsOrigWidthInc"  : ByteMap(68,   4, 'ulong'),
      #    "hintsOrigHeightInc" : ByteMap(72,   4, 'ulong'),
      #    "hintsMinWidth"      : ByteMap(76,   4, 'ulong'),
      #    "hintsMinHeight"     : ByteMap(80,   4, 'ulong'),
      #    "hintsMaxWidth"      : ByteMap(84,   4, 'ulong'),
      #    "hintsMaxHeight"     : ByteMap(88,   4, 'ulong'),
      #    "iconWindow"         : ByteMap(92,   4, 'ulong'),
      #    "iconPixmapWindow"   : ByteMap(96,   4, 'ulong'),
      #    "hintsWindowGravity" : ByteMap(100,  4, 'ulong'),
      #    "textPixel"          : ByteMap(104,  4, 'ulong'),
      #    "backPixel"          : ByteMap(108,  4, 'ulong'),
      #    "ewmhHintLayer"      : ByteMap(112,  4, 'ulong'),
      #    "ewmhHintDesktop"    : ByteMap(116,  4, 'ulong'),
      #    "ewmhWindowType"     : ByteMap(120,  4, 'ulong'),
      #    "titleHeight"        : ByteMap(124,  2, 'uint'),
      #    "borderWidth"        : ByteMap(126,  2, 'uint'),
      #    "DUMMY_0"            : ByteMap(128,  2, 'uint'),
      #    "DUMMY_1"            : ByteMap(130,  2, 'uint'),
           }
       },
   "M_CONFIGURE_WINDOW": {
       'pktType'  : 1 << 30,
       'pktUnion' : 'FvwmPkt.ConfigWinPacketUnion',
       'pktStruct': 'FvwmPkt.ConfigWinPacket',
       'pktSize'  : 'FvwmPkt.ConfigWinPacketSize',
       'pktStart' : 16,
       'pktVars'  : {
           # Rename some packet fields for consistency and clarity
           "windowId"   : 'w',
           "frameId"    : 'frame',
           "fvwmDbEntry": 'fvwmwin',

           # XXX This should be defined using the fvwm2 source code file
           #     libs/vpacket.h via a swig module!
           #"windowId"           : ByteMap(16,   4, 'ulong'),
           #"frameId"            : ByteMap(20,   4, 'int'),
           #"fvwmDbEntry"        : ByteMap(24,   4, 'ulong'), # Not Useful to us
           #"frameX"             : ByteMap(28,   4, 'int'),
           #"frameY"             : ByteMap(32,   4, 'int'),
           #"frameWidth"         : ByteMap(36,   4, 'ulong'),
           #"frameHeight"        : ByteMap(40,   4, 'ulong'),
           #"desk"               : ByteMap(44,   4, 'ulong'),
           #"layer"              : ByteMap(48,   4, 'ulong'),
           #"hintsBaseWidth"     : ByteMap(52,   4, 'ulong'),
           #"hintsBaseHeight"    : ByteMap(56,   4, 'ulong'),
           #"hintsWidthInc"      : ByteMap(60,   4, 'ulong'),
           #"hintsHeightInc"     : ByteMap(64,   4, 'ulong'),
           #"hintsOrigWidthInc"  : ByteMap(68,   4, 'ulong'),
           #"hintsOrigHeightInc" : ByteMap(72,   4, 'ulong'),
           #"hintsMinWidth"      : ByteMap(76,   4, 'ulong'),
           #"hintsMinHeight"     : ByteMap(80,   4, 'ulong'),
           #"hintsMaxWidth"      : ByteMap(84,   4, 'ulong'),
           #"hintsMaxHeight"     : ByteMap(88,   4, 'ulong'),
           #"iconWindow"         : ByteMap(92,   4, 'ulong'),
           #"iconPixmapWindow"   : ByteMap(96,   4, 'ulong'),
           #"hintsWindowGravity" : ByteMap(100,  4, 'ulong'),
           #"textPixel"          : ByteMap(104,  4, 'ulong'),
           #"backPixel"          : ByteMap(108,  4, 'ulong'),
           #"ewmhHintLayer"      : ByteMap(112,  4, 'ulong'),
           #"ewmhHintDesktop"    : ByteMap(116,  4, 'ulong'),
           #"ewmhWindowType"     : ByteMap(120,  4, 'ulong'),
           #"titleHeight"        : ByteMap(124,  2, 'uint'),
           #"borderWidth"        : ByteMap(126,  2, 'uint'),
           #"DUMMY_0"            : ByteMap(128,  2, 'uint'),
           #"DUMMY_1"            : ByteMap(130,  2, 'uint'),
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
           "windowId"    : ByteMap(16, 4,   'ulong'),
           "frameId"     : ByteMap(20, 4,   'int'),
           "fvwmDbEntry" : ByteMap(24, 4,   'ulong'), # Not Useful to us
           "name"        : ByteMap(28, None, StringVar) # Variable Length Character String
           }
       },
   "MX_ENTER_WINDOW": {
       'pktType': 1 <<  1 | 1 << 31,
       'pktVars': {
           "windowId"    : ByteMap(16, 4, 'ulong'),
           "frameId"     : ByteMap(20, 4, 'int'),
           "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
           }
       },
   "MX_LEAVE_WINDOW": {
       'pktType': 1 <<  2 | 1 << 31,
       'pktVars': {
           "windowId"    : ByteMap(16, 4, 'ulong'),
           "frameId"     : ByteMap(20, 4, 'int'),
           "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
           }
       },
    "MX_PROPERTY_CHANGE": {
        'pktType': 1 <<  3 | 1 << 31,
        'pktVars': {
            "type"        : ByteMap(16, 4, 'int'),
            "val1"        : ByteMap(20, 4, 'int'),
            "val2"        : ByteMap(24, 4, 'int'),
            "text"        : ByteMap(28, None, StringVar) # Variable Length Character String
            }
        },
    "MX_REPLY": {
        'pktType': 1 <<  4 | 1 << 31,
        'pktVars': {
            "windowId"    : ByteMap(16, 4, 'ulong'),
            "frameId"     : ByteMap(20, 4, 'int'),
            "fvwmDbEntry" : ByteMap(24, 4, 'ulong'), # Not Useful to us
            "text"        : ByteMap(28, None, StringVar) # Variable Length Character String
            }
        },
}

for name, definition in PacketTypes.items():
    definition['name'] = name
    PacketTypes[definition['pktType']] = definition
    exec("%(name)s=%(pktType)i" % definition)

def _GetLength(length): return uint(length) * 4

class FvwmModuleException(Exception): pass
class FvwmPacketException(FvwmModuleException): pass
class FvwmPacketIdException(FvwmPacketException): pass

class FvwmPacket(object):
    __metaclass__ =  ByteMapMeta
    syncpat       =  ByteMap(0,   4, ulong)
    packetType    =  ByteMap(4,   4, ulong)
    length        =  ByteMap(8,   4, (_GetLength,    None))
    time          =  ByteMap(12,  4, ulong)
    packetData    =  ByteMap(16, None)
    headerBytes   =  16
    pktClasses    =  {}

    TYPE_GENERIC  =  0
    TYPE_DIRECT   =  1
    TYPE_C_STRUCT =  2
    pktType       = TYPE_GENERIC

    varForm       = """    %(name)-13s= ByteMap(%(offset)i, %(length)s, %(conversion)s)\n"""
    redirForm     = """\
    %(name)s = property(lambda self: self.cPkt.packet.%(name)s,
                        lambda self, x: self.cPkt.packet.__setattr__("%(name)s", x))
"""
    cPktSetForm   = """
    def cPktSet(self, value):
        if len(value) > self.pktSize:
            raise ValueError, "ERROR setting packet %(name)s: Received %%i bytes, expected %%i" % (len(value), (self.headerBytes + self.pktSize))
        else:
            self.cPkt.data = value

"""

    classForm     = """
global FvwmPacket_%(name)s
class FvwmPacket_%(name)s(FvwmPacket):
    __metaclass__ =  ByteMapMeta
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
    def CreateClass(cls, name, pktType, pktVars, pktStruct=None, pktUnion=None, pktSize=None, pktStart=None):
        data = {
            "name"  : name,
            'type'  : pktType,
            "body"  : "",
            "fields": [],
            }
        if pktStruct is None:
            for name, value in pktVars.iteritems():
                data['body'] += cls.varForm % {
                    'name'      : name,
                    'offset'    : value.start,
                    'length'    : value.bytes,
                    'conversion': value.convert,
                    }
                data['fields'].append(name)
        else:
            data['body'] += "    pktType       = FvwmPacket.TYPE_C_STRUCT\n"
            data['body'] += "    pktSize       = %s\n" % pktSize
            data['body'] += "    pktUnion      = %s\n" % pktUnion
            data['body'] += "    pktStruct     = %s\n" % pktStruct
            data['body'] += "    cPkt          = %s()\n" % pktUnion

            cpkt   = eval('%s()' % pktStruct)
            fields = dir(cpkt)

            for field in fields:
                if not field.startswith('__'):
                    data['body'] += cls.redirForm % {'name': field}
                    data['fields'].append(field)

            for name, value in pktVars.iteritems():
                data['body'] += "    %s = %s\n" % (name, value)
                data['fields'].append(name)

            data['body'] += cls.cPktSetForm
        #end if

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

        self.registerCallback('M_STRING', self.onString)
        self.registerCommand('NOP', self.onNop)

        self.ParseOptionalArgs(*args)

        self.__PacketMonitor()

    def ParseOptionalArgs(self, *args):
        """Override this function to parse optional command-line arguments"""
        pass

    def __PacketMonitor(self):
        while not self.__exit:
            packet = FvwmPacket()
            packetHeader  = ''
            while len(packetHeader) < packet.headerBytes:
                received = self.fdRecv.read(packet.headerBytes)
                if len(received) > 0:
                    packetHeader += received
                else:
                    # We have been closed down, so exit the packet monitor
                    return
            packet.value  = packetHeader
            packetData    = self.fdRecv.read(packet.length - packet.headerBytes)
            packetClass   = packet.GetClass(packet.packetType)
            pkt           = packetClass()
            pkt.value     = packetHeader + packetData
            if pkt.pktType == FvwmPacket.TYPE_C_STRUCT:
                pkt.cPktSet(packetData)
            for (packetName, cbFunc) in self.__cbRegistry:
                if packetName == pkt.packetName or packetName == '*':
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

if __name__ == "__main__":
    module = FvwmModule(*sys.argv)

# vim:set ts=4 sw=4 et nu:
