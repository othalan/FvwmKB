################################################################################
# FVWM <=> Python Packet Communication Definitions
################################################################################

import ctypes
import FvwmCPkt

################################################################################
# Utility Class Definitions

class FvwmWindowIdentity(ctypes.Structure):
    _fields_ = [("windowId"   , ctypes.c_uint32),
                ("frameId"    , ctypes.c_int32 ),
                ("fvwmDbEntry", ctypes.c_uint32)]

class FvwmPktHeader(ctypes.Structure):
    _fields_ = [("syncpat"   , ctypes.c_uint32),
                ("packetType", ctypes.c_uint32),
                ("length"    , ctypes.c_uint32),
                ("time"      , ctypes.c_uint32)]

################################################################################
# Packet Definitions:
#
# "PKT_NAME" = {
#     'pktType': FVWM_PKT_ID,
#     'fields': FVWM_PKT_CONTENT,
# }
#
# FVWM_PKT_CONTENT = {
#    VAR_NAME: [BYTE_OFFSET, BYTE_LENGTH, DATA_TYPE],
# }

PacketTypes = {
   FvwmCPkt.M_NEW_PAGE: {
        'name': "M_NEW_PAGE",
        'type': "static",
        'fields': [
            ("vpX"   , ctypes.c_int32),
            ("vpY"   , ctypes.c_int32),
            ("desk"  , ctypes.c_int32),
            ("width" , ctypes.c_int32),
            ("height", ctypes.c_int32),
            ("vpXnum", ctypes.c_int32),
            ("vpYnum", ctypes.c_int32),
            ]
        },
   FvwmCPkt.M_NEW_DESK: {
        'name': "M_NEW_DESK",
        'type': "static",
        'fields': [
            ("desk"  , ctypes.c_int32),
            ]
        },
   FvwmCPkt.M_OLD_ADD_WINDOW: {
        'name': "M_OLD_ADD_WINDOW",
        'type': "static",
        'fields': [
            ]
        },
   FvwmCPkt.M_RAISE_WINDOW: {
        'name': "M_RAISE_WINDOW",
        'type': "static",
        'fields': [
            ("windowId"    , ctypes.c_uint32),
            ("frameId"     , ctypes.c_int32),
            ("fvwmDbEntry" , ctypes.c_uint32), # Not Useful to us
            ]
        },
   FvwmCPkt.M_LOWER_WINDOW: {
        'name': "M_LOWER_WINDOW",
        'type': "static",
        'fields': [
            ("windowId"    , ctypes.c_uint32),
            ("frameId"     , ctypes.c_int32),
            ("fvwmDbEntry" , ctypes.c_uint32), # Not Useful to us
            ]
        },
   FvwmCPkt.M_OLD_CONFIGURE_WINDOW: {
        'name': "M_OLD_CONFIGURE_WINDOW",
        'type': "static",
        'fields': [
            ]
        },
   FvwmCPkt.M_FOCUS_CHANGE: {
        'name': "M_FOCUS_CHANGE",
        'type': "static",
        'fields': [
            ("windowId"    , ctypes.c_uint32),
            ("frameId"     , ctypes.c_int32),
            ("changeType"  , ctypes.c_uint32),
            ("colorHlText" , ctypes.c_int32),
            ("colorHlBg"   , ctypes.c_int32),
            ]
        },
   FvwmCPkt.M_DESTROY_WINDOW: {
        'name': "M_DESTROY_WINDOW",
        'type': "static",
        'fields': [
            ("windowId"    , ctypes.c_uint32),
            ("frameId"     , ctypes.c_int32),
            ("fvwmDbEntry" , ctypes.c_uint32), # Not Useful to us
            ]
        },
   FvwmCPkt.M_ICONIFY: {
        'name': "M_ICONIFY",
        'type': "static",
        'fields': [
            ("windowId"    , ctypes.c_uint32),
            ("frameId"     , ctypes.c_int32),
            ("fvwmDbEntry" , ctypes.c_uint32), # Not Useful to us
            ("iconXPos"    , ctypes.c_int32),
            ("iconYPos"    , ctypes.c_int32),
            ("iconWidth"   , ctypes.c_int32),
            ("iconHeight"  , ctypes.c_int32),
            ("frameXPos"   , ctypes.c_int32),
            ("frameYPos"   , ctypes.c_int32),
            ("frameWidth"  , ctypes.c_int32),
            ("frameHeight" , ctypes.c_int32),
            ]
        },
   FvwmCPkt.M_DEICONIFY: {
        'name': "M_DEICONIFY",
        'type': "static",
        'fields': [
            ("windowId"    , ctypes.c_uint32),
            ("frameId"     , ctypes.c_int32),
            ("fvwmDbEntry" , ctypes.c_uint32), # Not Useful to us
            ("iconXPos"    , ctypes.c_int32),
            ("iconYPos"    , ctypes.c_int32),
            ("iconWidth"   , ctypes.c_int32),
            ("iconHeight"  , ctypes.c_int32),
            ("frameXPos"   , ctypes.c_int32),
            ("frameYPos"   , ctypes.c_int32),
            ("frameWidth"  , ctypes.c_int32),
            ("frameHeight" , ctypes.c_int32),
            ]
        },
   FvwmCPkt.M_WINDOW_NAME: {
        'name': "M_WINDOW_NAME",
        'type': "dynamic",
        'fields': [
            ("windowId"   , ctypes.c_uint32),
            ("frameId"    , ctypes.c_int32),
            ("fvwmDbEntry", ctypes.c_uint32), # Not Useful to us
            ("name"       , ctypes.c_char*1) # Variable Length Character String
            ]
        },
   FvwmCPkt.M_ICON_NAME: {
        'name': "M_ICON_NAME",
        'type': "dynamic",
        'fields': [
            ("windowId"   , ctypes.c_uint32),
            ("frameId"    , ctypes.c_int32),
            ("fvwmDbEntry", ctypes.c_uint32), # Not Useful to us
            ("name"       , ctypes.c_char*1) # Variable Length Character String
            ]
        },
   FvwmCPkt.M_RES_CLASS: {
        'name': "M_RES_CLASS",
        'type': "dynamic",
        'fields': [
            ("windowId"   , ctypes.c_uint32),
            ("frameId"    , ctypes.c_int32),
            ("fvwmDbEntry", ctypes.c_uint32), # Not Useful to us
            ("name"       , ctypes.c_char*1) # Variable Length Character String
            ]
        },
   FvwmCPkt.M_RES_NAME: {
        'name': "M_RES_NAME",
        'type': "dynamic",
        'fields': [
            ("windowId"   , ctypes.c_uint32),
            ("frameId"    , ctypes.c_int32),
            ("fvwmDbEntry", ctypes.c_uint32), # Not Useful to us
            ("name"       , ctypes.c_char*1) # Variable Length Character String
            ]
        },
   FvwmCPkt.M_END_WINDOWLIST: {
        'name': "M_END_WINDOWLIST",
        'type': "static",
        'fields': [
            # No Values
            ]
        },
   FvwmCPkt.M_ICON_LOCATION: {
        'name': "M_ICON_LOCATION",
        'type': "static",
        'fields': [
            ("windowId"    , ctypes.c_uint32),
            ("frameId"     , ctypes.c_int32),
            ("fvwmDbEntry" , ctypes.c_uint32), # Not Useful to us
            ("xPos"        , ctypes.c_int32),
            ("yPos"        , ctypes.c_int32),
            ("width"       , ctypes.c_int32),
            ("height"      , ctypes.c_int32),
            ]
        },
   FvwmCPkt.M_MAP: {
        'name': "M_MAP",
        'type': "static",
        'fields': [
            ("windowId"    , ctypes.c_uint32),
            ("frameId"     , ctypes.c_int32),
            ("fvwmDbEntry" , ctypes.c_uint32), # Not Useful to us
            ]
        },
   FvwmCPkt.M_ERROR: {
        'name': "M_ERROR",
        'type': "static",
        'fields': [
            ("DUMMY_0"    , ctypes.c_int32),
            ("DUMMY_1"    , ctypes.c_int32),
            ("DUMMY_2"    , ctypes.c_int32),
            ("error"      , ctypes.c_char*1) # Variable Length Character String
            ]
        },
   FvwmCPkt.M_CONFIG_INFO: {
        'name': "M_CONFIG_INFO",
        'type': "dynamic",
        'fields': [
            ("DUMMY_0"    , ctypes.c_int32),
            ("DUMMY_1"    , ctypes.c_int32),
            ("DUMMY_2"    , ctypes.c_int32),
            ("text"       , ctypes.c_char*1) # Variable Length Character String
            ]
        },
   FvwmCPkt.M_END_CONFIG_INFO: {
        'name': "M_END_CONFIG_INFO",
        'type': "static",
        'fields': [
            # No Values
            ]
        },
   FvwmCPkt.M_ICON_FILE: {
        'name': "M_ICON_FILE",
        'type': "dynamic",
        'fields': [
            ("windowId"    , ctypes.c_uint32),
            ("frameId"     , ctypes.c_int32),
            ("fvwmDbEntry" , ctypes.c_uint32), # Not Useful to us
            ("name"        , ctypes.c_char*1) # Variable Length Character String
            ]
        },
   FvwmCPkt.M_DEFAULTICON: {
        'name': "M_DEFAULTICON",
        'type': "dynamic",
        'fields': [
            ("name"        , ctypes.c_char*1) # Variable Length Character String
            ]
        },
   FvwmCPkt.M_STRING: {
        'name': "M_STRING",
        'type': "dynamic",
        'fields': [
            ("windowId"    , ctypes.c_uint32),
            ("frameId"     , ctypes.c_int32),
            ("fvwmDbEntry" , ctypes.c_uint32), # Not Useful to us
            ("text"        , ctypes.c_char*1) # Variable Length Character String
            ]
        },
   FvwmCPkt.M_MINI_ICON: {
        'name': "M_MINI_ICON",
        'type': "swig",
        'pktUnion' : 'FvwmCPkt.MiniIconPacketUnion',
        'pktStruct': 'FvwmCPkt.MiniIconPacket',
        'pktSize'  : 'FvwmCPkt.MiniIconPacketSize',
        'pktStart' : 16,
        'fields'   : {
            # Rename some packet fields for consistency and clarity
            "windowId"   : 'w',
            "frameId"    : 'frame',
            "fvwmDbEntry": 'fvwmwin',
            }
        },
   FvwmCPkt.M_WINDOWSHADE: {
        'name': "M_WINDOWSHADE",
        'type': "static",
        'fields': {
            ("windowId"    , ctypes.c_uint32),
            ("frameId"     , ctypes.c_int32),
            ("fvwmDbEntry" , ctypes.c_uint32), # Not Useful to us
            }
        },
   FvwmCPkt.M_DEWINDOWSHADE: {
        'name': "M_DEWINDOWSHADE",
        'type': "static",
        'fields': [
            ("windowId"    , ctypes.c_uint32),
            ("frameId"     , ctypes.c_int32),
            ("fvwmDbEntry" , ctypes.c_uint32), # Not Useful to us
            ]
        },
   FvwmCPkt.M_VISIBLE_NAME: {
        'name': "M_VISIBLE_NAME",
        'type': "dynamic",
        'fields': [
            ("windowId"    , ctypes.c_uint32),
            ("frameId"     , ctypes.c_int32),
            ("fvwmDbEntry" , ctypes.c_uint32), # Not Useful to us
            ("name"        , ctypes.c_char*1) # Variable Length Character String
            ]
        },
    FvwmCPkt.M_SENDCONFIG: {
        'name': "M_SENDCONFIG",
        'type': "static",
        'fields': [
            # Never sent by FVWM
            ]
        },
    FvwmCPkt.M_RESTACK: {
        'name': "M_RESTACK",
        'type': "dynamic",
        'fields': [
            ("windowList", FvwmWindowIdentity*1),
            ]
        },
   FvwmCPkt.M_ADD_WINDOW: {
        'name'  : "M_ADD_WINDOW",
        'type': "swig",
        'pktUnion' : 'FvwmCPkt.ConfigWinPacketUnion',
        'pktStruct': 'FvwmCPkt.ConfigWinPacket',
        'pktSize'  : 'FvwmCPkt.ConfigWinPacketSize',
        'pktStart' : 16,
        'fields'  : {
            # Rename some packet fields for consistency and clarity
            "windowId"   : 'w',
            "frameId"    : 'frame',
            "fvwmDbEntry": 'fvwmwin',
            }
        },
   FvwmCPkt.M_CONFIGURE_WINDOW: {
        'name'     : "M_CONFIGURE_WINDOW",
        'type'     : "swig",
        'pktUnion' : 'FvwmCPkt.ConfigWinPacketUnion',
        'pktStruct': 'FvwmCPkt.ConfigWinPacket',
        'pktSize'  : 'FvwmCPkt.ConfigWinPacketSize',
        'pktStart' : 16,
        'fields'  : {
            # Rename some packet fields for consistency and clarity
            "windowId"   : 'w',
            "frameId"    : 'frame',
            "fvwmDbEntry": 'fvwmwin',
            }
        },
    FvwmCPkt.M_EXTENDED_MSG: {
        'name': "M_EXTENDED_MSG",
        'type': "static",
        'fields': [
            ]
        },
   FvwmCPkt.MX_VISIBLE_ICON_NAME: {
        'name': "MX_VISIBLE_ICON_NAME",
        'type': "dynamic",
        'fields': [
            ("windowId"    , ctypes.c_uint32),
            ("frameId"     , ctypes.c_int32),
            ("fvwmDbEntry" , ctypes.c_uint32), # Not Useful to us
            ("name"        , ctypes.c_char*1) # Variable Length Character String
            ]
        },
   FvwmCPkt.MX_ENTER_WINDOW: {
        'name': "MX_ENTER_WINDOW",
        'type': "static",
        'fields': [
            ("windowId"    , ctypes.c_uint32),
            ("frameId"     , ctypes.c_int32),
            ("fvwmDbEntry" , ctypes.c_uint32), # Not Useful to us
            ]
        },
   FvwmCPkt.MX_LEAVE_WINDOW: {
        'name': "MX_LEAVE_WINDOW",
        'type': "static",
        'fields': [
            ("windowId"    , ctypes.c_uint32),
            ("frameId"     , ctypes.c_int32),
            ("fvwmDbEntry" , ctypes.c_uint32), # Not Useful to us
            ]
        },
    FvwmCPkt.MX_PROPERTY_CHANGE: {
        'name': "MX_PROPERTY_CHANGE",
        'type': "dynamic",
        'fields': [
            ("type"        , ctypes.c_int32),
            ("val1"        , ctypes.c_int32),
            ("val2"        , ctypes.c_int32),
            ("text"        , ctypes.c_char*1) # Variable Length Character String
            ]
        },
    FvwmCPkt.MX_REPLY: {
        'name': "MX_REPLY",
        'type': "dynamic",
        'fields': [
            ("windowId"    , ctypes.c_uint32),
            ("frameId"     , ctypes.c_int32),
            ("fvwmDbEntry" , ctypes.c_uint32), # Not Useful to us
            ("text"        , ctypes.c_char*1) # Variable Length Character String
            ]
        },
}

################################################################################
# Fill out the configuration dictionary so it is a bit more useful by
# adding id-name two-way lookup.

def __setup():
    pktIds = PacketTypes.keys()
    for pktId in pktIds:
        pktDict = PacketTypes[pktId]
        pktDict['id'] = pktId
        PacketTypes[pktDict['name']] = pktDict

        # XXX Should the header be inserted at the beginning?
        #if pktDict['type'] in ('static', 'dynamic'):
        #    pktDict['fields'].insert(0,('header', FvwmPktHeader))
__setup()

################################################################################
# Dynamic Class Templates


################################################################################
# Utility Functions

def get_fvwm_pkt_obj(pktType, pktLen = -1):
    ctypes_packet_class = """
global FvwmPkt_%(name)s_Struct
global FvwmPkt_%(name)s

class FvwmPkt_%(name)s_Struct(ctypes.Structure):
    _fields_ = pktDict['fields']
class FvwmPkt_%(name)s(ctypes.Union):
    _fields_ = [("struct", FvwmPkt_%(name)s_Struct),
                ("data",   ctypes.c_byte * ctypes.sizeof(FvwmPkt_%(name)s_Struct))]
"""

    global pktDict
    pktDict = PacketTypes[pktType]
    if pktLen >= 0:
        if pktDict['type'] != 'dynamic':
            raise TypeError, "Attempt to resize non-resizeable FVWM Packet!"

        # Calculate the packet base size if needed...
        if pktDict['baseSize'] == -1:
            resizeable = pktDict['fields'][-1]
            pktDict['fields'] = pktDict['fields'][:]
            exec ctypes_packet_class % pktDict
            pktDict['fields'].append(resizeable)
            pktDict['baseSize'] = ctypes.sizeof(eval('FvwmPkt_%(name)s_Struct' % pktDict))

        # Calculate the packet current size...
        pktDict['fields'][-1] = (pktDict['fields'][-1][0],
                                 ctypes.c_char * (pktLen - pktDict['baseSize']))

        # Crete the new class
        exec ctypes_packet_class % pktDict
        pktDict['class'] = eval('FvwmPkt_%(name)s' % pktDict)

    elif not pktDict.has_key('class') and pktDict['type'] == 'static':
        exec ctypes_packet_class % pktDict
        pktDict['class'] = eval('FvwmPkt_%(name)s' % pktDict)

    elif not pktDict.has_key('class') and pktDict['type'] == 'swig':
        raise NotImplemented, "ERROR:  Swig Classes Not Yet Implemented!"

    # Create the object and return it
    return pktDict['class']()


