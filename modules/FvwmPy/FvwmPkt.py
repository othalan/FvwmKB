################################################################################
# FVWM <=> Python Packet Communication Definitions
################################################################################

import ctypes
import math
import sys
import FvwmCPkt

PKT_TYPE_STATIC  = "static"
PKT_TYPE_DYNAMIC = "dynamic"
PKT_TYPE_SWIG    = "swig"

################################################################################
# Utility Class Definitions

class FvwmWindowIdentity(ctypes.Structure):
    _fields_ = [("windowId"   , ctypes.c_uint32),
                ("frameId"    , ctypes.c_int32 ),
                ("fvwmDbEntry", ctypes.c_uint32)]

class FvwmPktBase(ctypes.Structure):
    data     = property(lambda self  : self.__getData(),
                        lambda self,x: self.__setData(x),
                        None,
                        "Packet data as a character array")

    fields   = property(lambda self  : self.__getFields(),
                        None,
                        None,
                        "List of structure fields for this packet")

    def __getData(self):
        source=ctypes.cast(ctypes.pointer(self),ctypes.POINTER(ctypes.c_char))
        return ''.join([source[ix] for ix in xrange(len(self))])

    def __setData(self, toSet):
        target=ctypes.cast(ctypes.pointer(self),ctypes.POINTER(ctypes.c_char))
        for ix in xrange(min(len(toSet),len(self))):
            target[ix]=toSet[ix]

    def __len__(self):
        return ctypes.sizeof(self)

    def __getitem__(self, key):
        if key in self.fields:
            keypath = key.split(':')
            if keypath[0] == 'header':
                value = getattr(self.header, keypath[1])
            else:
                value = self
                for realkey in keypath:
                    value = getattr(value, realkey)
            return value
        else:
            raise KeyError, "Invalid Field Name: %s" % key

    def __setitem__(self, key, value):
        if key in self.fields:
            keypath = key.split(':')
            if keypath[0] == 'header':
                setattr(self.header, keypath[1], value)
            else:
                obj = self
                for realkey in keypath[:-1]:
                    obj = getattr(obj, realkey)
                setattr(obj, keypath[-1], value)
        else:
            raise KeyError, "Invalid Field Name: %s" % key

    def __getFields(self):
        if not hasattr(self, '_field_list'):
            self._field_list = [field[0].lstrip('_') for field in self._fields_]
            if hasattr(self, 'header'):
                self._field_list.remove('header')
                self._field_list.extend(['header:%s'%field for field in self.header.fields])
            self._field_list.sort()
        return self._field_list

class FvwmPktHeader(FvwmPktBase):
    """
FVWM Packet Header Structure

NOTE:  The 'length' field represents the total packet length in bytes!
       The FVWM module protocol provides the number of 4-byte words,
       however the number of bytes is a more useful number in Python
       so the calculation is being handled automatically.
"""
    _fields_ = [("_syncpat" , ctypes.c_uint32),
                ("_type"    , ctypes.c_uint32),
                ("_length"  , ctypes.c_uint32),
                ("_time"    , ctypes.c_uint32)]

    syncpat  = property(lambda self  : self._syncpat,
                        lambda self,x: self.__setattr__("_syncpat", x),
                        None,
                        "Packet Sync Pattern (expected 0xFFFFFFFF)")
    type     = property(lambda self  : self._type,
                        lambda self,x: self.__setattr__("_type", x),
                        None,
                        "Packet Type Code")
    length   = property(lambda self  : self._length*4,
                        lambda self,x: self.__setattr__("_length", int(math.ceil(x/4.0))),
                        None,
                        "Actual packet length in BYTES")
    raw_length = property(lambda self  : self._length,
                        lambda self,x: self.__setattr__("_length", x),
                        None,
                        "Actual packet length in 4-BYTE WORDS")
    time     = property(lambda self  : self._time,
                        lambda self,x: self.__setattr__("_time", x),
                        None,
                        "Packet Time in Microseconds")

    def __getitem__(self, key):
        if key == 'raw_length':
            return getattr(self, key)
        else:
            return super(FvwmPktHeader,self).__getitem__(key)

class FvwmSwigMeta(type):
    def __new__(cls, name, bases, dct):
        dct['cstruct'] = property(
                    lambda self  : self._cstruct,
                    None,
                    None,
                    "SWIG C Structure direct access")
        dct['header'] = property(
                    lambda self  : self._header,
                    lambda self,x: setattr(self,'_header',x),
                    None,
                    "Packet header structure")
        def setPktData(self, data):
            self.header.data  = data[:len(self.header)]
            self.cstruct.data = data[len(self.header):]
        dct['data'] = property(
                    lambda self  : self.header.data + self.cstruct._getData(),
                    lambda self,x: setPktData(self,x),
                    None,
                    "Packet raw data (including header and data portions of the packet)")
        dct['_cstruct']    = dct['_swigClass']()
        dct['header']      = FvwmPktHeader()
        dct['fields']      = ['header:%s'%field for field in dct['header'].fields]
        dct['__getitem__'] = cls.__getitem
        dct['__setitem__'] = cls.__setitem

        for attr in dct['_swigClass'].__dict__.keys():
            if not attr.startswith('_'):
                # Note that the lambda function would normally use the global
                # scope 'attr' variable (thus referring to the last item in the
                # loop), so we must copy it to the lambda function local scope
                # to refer to the current loop value of the variable.
                dct[attr] = property(lambda self,attr=attr  : getattr(self._cstruct, attr),
                                     lambda self,x,attr=attr: setattr(self._cstruct, attr, x))

                # Recursively add structure members to the list of available dictionary fields....
                def addDictVals(obj, toGet, strSoFar):
                    attrVal = getattr(obj, toGet)
                    if hasattr(attrVal, '__swig_getmethods__'):
                        for field in attrVal.__class__.__dict__.keys():
                            if not field.startswith('_'):
                                addDictVals(attrVal, field, '%s:%s' % (strSoFar,field))
                    else:
                        dct['fields'].append(strSoFar)

                addDictVals(dct['_cstruct'], attr, attr)
        dct['fields'].sort()

        return super(FvwmSwigMeta, cls).__new__(cls, name, bases, dct)

    @staticmethod
    def __getitem(self, key):
        if key in self.fields:
            keypath = key.split(':')
            if keypath[0] == 'header':
                value = getattr(self.header, keypath[1])
            else:
                value = self._cstruct
                for realkey in keypath:
                    value = getattr(value, realkey)
            return value
        else:
            raise KeyError, "Invalid Field Name: %s" % key

    @staticmethod
    def __setitem(self, key, value):
        if key in self.fields:
            keypath = key.split(':')
            if keypath[0] == 'header':
                setattr(self.header, keypath[1], value)
            else:
                obj = self._cstruct
                for realkey in keypath[:-1]:
                    obj = getattr(obj, realkey)
                setattr(obj, keypath[-1], value)
        else:
            raise KeyError, "Invalid Field Name: %s" % key

################################################################################
# Packet Definitions:

PacketTypes = {
   FvwmCPkt.M_NEW_PAGE: {
        'name': "M_NEW_PAGE",
        'type': "static",
        'fields': [
            ("vpX"   , 'ctypes.c_int32'),
            ("vpY"   , 'ctypes.c_int32'),
            ("desk"  , 'ctypes.c_int32'),
            ("width" , 'ctypes.c_int32'),
            ("height", 'ctypes.c_int32'),
            ("vpXnum", 'ctypes.c_int32'),
            ("vpYnum", 'ctypes.c_int32'),
            ]
        },
   FvwmCPkt.M_NEW_DESK: {
        'name': "M_NEW_DESK",
        'type': "static",
        'fields': [
            ("desk"  , 'ctypes.c_int32'),
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
            ("windowId"    , 'ctypes.c_uint32'),
            ("frameId"     , 'ctypes.c_int32'),
            ("fvwmDbEntry" , 'ctypes.c_uint32'), # Not Useful to us
            ]
        },
   FvwmCPkt.M_LOWER_WINDOW: {
        'name': "M_LOWER_WINDOW",
        'type': "static",
        'fields': [
            ("windowId"    , 'ctypes.c_uint32'),
            ("frameId"     , 'ctypes.c_int32'),
            ("fvwmDbEntry" , 'ctypes.c_uint32'), # Not Useful to us
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
            ("windowId"    , 'ctypes.c_uint32'),
            ("frameId"     , 'ctypes.c_int32'),
            ("changeType"  , 'ctypes.c_uint32'),
            ("colorHlText" , 'ctypes.c_int32'),
            ("colorHlBg"   , 'ctypes.c_int32'),
            ]
        },
   FvwmCPkt.M_DESTROY_WINDOW: {
        'name': "M_DESTROY_WINDOW",
        'type': "static",
        'fields': [
            ("windowId"    , 'ctypes.c_uint32'),
            ("frameId"     , 'ctypes.c_int32'),
            ("fvwmDbEntry" , 'ctypes.c_uint32'), # Not Useful to us
            ]
        },
   FvwmCPkt.M_ICONIFY: {
        'name': "M_ICONIFY",
        'type': "static",
        'fields': [
            ("windowId"    , 'ctypes.c_uint32'),
            ("frameId"     , 'ctypes.c_int32'),
            ("fvwmDbEntry" , 'ctypes.c_uint32'), # Not Useful to us
            ("iconXPos"    , 'ctypes.c_int32'),
            ("iconYPos"    , 'ctypes.c_int32'),
            ("iconWidth"   , 'ctypes.c_int32'),
            ("iconHeight"  , 'ctypes.c_int32'),
            ("frameXPos"   , 'ctypes.c_int32'),
            ("frameYPos"   , 'ctypes.c_int32'),
            ("frameWidth"  , 'ctypes.c_int32'),
            ("frameHeight" , 'ctypes.c_int32'),
            ]
        },
   FvwmCPkt.M_DEICONIFY: {
        'name': "M_DEICONIFY",
        'type': "static",
        'fields': [
            ("windowId"    , 'ctypes.c_uint32'),
            ("frameId"     , 'ctypes.c_int32'),
            ("fvwmDbEntry" , 'ctypes.c_uint32'), # Not Useful to us
            ("iconXPos"    , 'ctypes.c_int32'),
            ("iconYPos"    , 'ctypes.c_int32'),
            ("iconWidth"   , 'ctypes.c_int32'),
            ("iconHeight"  , 'ctypes.c_int32'),
            ("frameXPos"   , 'ctypes.c_int32'),
            ("frameYPos"   , 'ctypes.c_int32'),
            ("frameWidth"  , 'ctypes.c_int32'),
            ("frameHeight" , 'ctypes.c_int32'),
            ]
        },
   FvwmCPkt.M_WINDOW_NAME: {
        'name': "M_WINDOW_NAME",
        'type': "dynamic",
        'fields': [
            ("windowId"   , 'ctypes.c_uint32'),
            ("frameId"    , 'ctypes.c_int32'),
            ("fvwmDbEntry", 'ctypes.c_uint32'), # Not Useful to us
            ("name"       , 'ctypes.c_char*1') # Variable Length Character String
            ]
        },
   FvwmCPkt.M_ICON_NAME: {
        'name': "M_ICON_NAME",
        'type': "dynamic",
        'fields': [
            ("windowId"   , 'ctypes.c_uint32'),
            ("frameId"    , 'ctypes.c_int32'),
            ("fvwmDbEntry", 'ctypes.c_uint32'), # Not Useful to us
            ("name"       , 'ctypes.c_char*1') # Variable Length Character String
            ]
        },
   FvwmCPkt.M_RES_CLASS: {
        'name': "M_RES_CLASS",
        'type': "dynamic",
        'fields': [
            ("windowId"   , 'ctypes.c_uint32'),
            ("frameId"    , 'ctypes.c_int32'),
            ("fvwmDbEntry", 'ctypes.c_uint32'), # Not Useful to us
            ("name"       , 'ctypes.c_char*1') # Variable Length Character String
            ]
        },
   FvwmCPkt.M_RES_NAME: {
        'name': "M_RES_NAME",
        'type': "dynamic",
        'fields': [
            ("windowId"   , 'ctypes.c_uint32'),
            ("frameId"    , 'ctypes.c_int32'),
            ("fvwmDbEntry", 'ctypes.c_uint32'), # Not Useful to us
            ("name"       , 'ctypes.c_char*1') # Variable Length Character String
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
            ("windowId"    , 'ctypes.c_uint32'),
            ("frameId"     , 'ctypes.c_int32'),
            ("fvwmDbEntry" , 'ctypes.c_uint32'), # Not Useful to us
            ("xPos"        , 'ctypes.c_int32'),
            ("yPos"        , 'ctypes.c_int32'),
            ("width"       , 'ctypes.c_int32'),
            ("height"      , 'ctypes.c_int32'),
            ]
        },
   FvwmCPkt.M_MAP: {
        'name': "M_MAP",
        'type': "static",
        'fields': [
            ("windowId"    , 'ctypes.c_uint32'),
            ("frameId"     , 'ctypes.c_int32'),
            ("fvwmDbEntry" , 'ctypes.c_uint32'), # Not Useful to us
            ]
        },
   FvwmCPkt.M_ERROR: {
        'name': "M_ERROR",
        'type': "static",
        'fields': [
            ("DUMMY_0"    , 'ctypes.c_int32'),
            ("DUMMY_1"    , 'ctypes.c_int32'),
            ("DUMMY_2"    , 'ctypes.c_int32'),
            ("error"      , 'ctypes.c_char*1') # Variable Length Character String
            ]
        },
   FvwmCPkt.M_CONFIG_INFO: {
        'name': "M_CONFIG_INFO",
        'type': "dynamic",
        'fields': [
            ("DUMMY_0"    , 'ctypes.c_int32'),
            ("DUMMY_1"    , 'ctypes.c_int32'),
            ("DUMMY_2"    , 'ctypes.c_int32'),
            ("text"       , 'ctypes.c_char*1') # Variable Length Character String
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
            ("windowId"    , 'ctypes.c_uint32'),
            ("frameId"     , 'ctypes.c_int32'),
            ("fvwmDbEntry" , 'ctypes.c_uint32'), # Not Useful to us
            ("name"        , 'ctypes.c_char*1') # Variable Length Character String
            ]
        },
   FvwmCPkt.M_DEFAULTICON: {
        'name': "M_DEFAULTICON",
        'type': "dynamic",
        'fields': [
            ("name"        , 'ctypes.c_char*1') # Variable Length Character String
            ]
        },
   FvwmCPkt.M_STRING: {
        'name': "M_STRING",
        'type': "dynamic",
        'fields': [
            ("windowId"    , 'ctypes.c_uint32'),
            ("frameId"     , 'ctypes.c_int32'),
            ("fvwmDbEntry" , 'ctypes.c_uint32'), # Not Useful to us
            ("text"        , 'ctypes.c_char*1') # Variable Length Character String
            ]
        },
   FvwmCPkt.M_MINI_ICON: {
        'name'     : "M_MINI_ICON",
        'type'     : "swig",
        'swigType' : 'FvwmCPkt.MiniIconPacket',
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
        'fields': [
            ("windowId"    , 'ctypes.c_uint32'),
            ("frameId"     , 'ctypes.c_int32'),
            ("fvwmDbEntry" , 'ctypes.c_uint32'), # Not Useful to us
            ]
        },
   FvwmCPkt.M_DEWINDOWSHADE: {
        'name': "M_DEWINDOWSHADE",
        'type': "static",
        'fields': [
            ("windowId"    , 'ctypes.c_uint32'),
            ("frameId"     , 'ctypes.c_int32'),
            ("fvwmDbEntry" , 'ctypes.c_uint32'), # Not Useful to us
            ]
        },
   FvwmCPkt.M_VISIBLE_NAME: {
        'name': "M_VISIBLE_NAME",
        'type': "dynamic",
        'fields': [
            ("windowId"    , 'ctypes.c_uint32'),
            ("frameId"     , 'ctypes.c_int32'),
            ("fvwmDbEntry" , 'ctypes.c_uint32'), # Not Useful to us
            ("name"        , 'ctypes.c_char*1') # Variable Length Character String
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
        'name'    : "M_ADD_WINDOW",
        'type'    : "swig",
        'swigType': 'FvwmCPkt.ConfigWinPacket',
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
        'swigType' : 'FvwmCPkt.ConfigWinPacket',
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
            ("windowId"    , 'ctypes.c_uint32'),
            ("frameId"     , 'ctypes.c_int32'),
            ("fvwmDbEntry" , 'ctypes.c_uint32'), # Not Useful to us
            ("name"        , 'ctypes.c_char*1') # Variable Length Character String
            ]
        },
   FvwmCPkt.MX_ENTER_WINDOW: {
        'name': "MX_ENTER_WINDOW",
        'type': "static",
        'fields': [
            ("windowId"    , 'ctypes.c_uint32'),
            ("frameId"     , 'ctypes.c_int32'),
            ("fvwmDbEntry" , 'ctypes.c_uint32'), # Not Useful to us
            ]
        },
   FvwmCPkt.MX_LEAVE_WINDOW: {
        'name': "MX_LEAVE_WINDOW",
        'type': "static",
        'fields': [
            ("windowId"    , 'ctypes.c_uint32'),
            ("frameId"     , 'ctypes.c_int32'),
            ("fvwmDbEntry" , 'ctypes.c_uint32'), # Not Useful to us
            ]
        },
    FvwmCPkt.MX_PROPERTY_CHANGE: {
        'name': "MX_PROPERTY_CHANGE",
        'type': "dynamic",
        'fields': [
            ("type"        , 'ctypes.c_int32'),
            ("val1"        , 'ctypes.c_int32'),
            ("val2"        , 'ctypes.c_int32'),
            ("text"        , 'ctypes.c_char*1') # Variable Length Character String
            ]
        },
    FvwmCPkt.MX_REPLY: {
        'name': "MX_REPLY",
        'type': "dynamic",
        'fields': [
            ("windowId"    , 'ctypes.c_uint32'),
            ("frameId"     , 'ctypes.c_int32'),
            ("fvwmDbEntry" , 'ctypes.c_uint32'), # Not Useful to us
            ("text"        , 'ctypes.c_char*1') # Variable Length Character String
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

        if not pktDict.has_key('doc'):
            pktDict['doc'] = ''

        if pktDict['type'] in ('static', 'dynamic'):
            pktDict['fields'].insert(0,('header', 'FvwmPktHeader'))
__setup()

################################################################################
# Dynamic Class Templates


################################################################################
# Utility Functions

def __build_field_str(pktDef):
    fieldStr = '['
    for name,ftype in pktDef['fields']:
        fieldStr += '("%s",%s),' % (name,ftype)
    fieldStr += ']'
    pktDef['field_str'] = fieldStr

def __createSwigStrict(pktDef):
    swig_packet_class = """
global FvwmPkt_%(name)s
global %(name)s

%(name)s = %(id)s

class FvwmPkt_%(name)s(object):
    __metaclass__ = FvwmSwigMeta
    __doc__       = "%(doc)s"
    _swigClass    = %(swigType)s
    _name         = "%(name)s"
    _id           = %(id)s
    _type         = "%(type)s"

    name     = property(lambda self  : self._name,
                        None,
                        None,
                        "Packet Name (from FVWM Documentation)")
    id       = property(lambda self  : self._id,
                        None,
                        None,
                        "Packet ID Value (from FVWM Header Files)")
    type     = property(lambda self  : self._type,
                        None,
                        None,
                        "Packet definition type code")
"""
    code = compile(swig_packet_class % pktDef, "<string>", "exec")
    exec code in globals(), locals()
    pktDef['class'] = eval('FvwmPkt_%(name)s' % pktDef)

def __createCtypeStruct(pktDef):
    ctypes_packet_class = """
global FvwmPkt_%(name)s
global %(name)s

# Create a constant for this packet name
%(name)s = %(id)s

# Create a class structure for this packet
class FvwmPkt_%(name)s(FvwmPktBase):
    __doc__  = "%(doc)s"
    _fields_ = %(field_str)s
    _name    = "%(name)s"
    _id      = %(id)s
    _type    = "%(type)s"

    name     = property(lambda self  : self._name,
                        None,
                        None,
                        "Packet Name (from FVWM Documentation)")
    id       = property(lambda self  : self._id,
                        None,
                        None,
                        "Packet ID Value (from FVWM Header Files)")
    type     = property(lambda self  : self._type,
                        None,
                        None,
                        "Packet definition type code")
"""
    __build_field_str(pktDef)
    code = compile(ctypes_packet_class % pktDef, "<string>", "exec")
    exec code in globals(), locals()
    pktDef['class'] = eval('FvwmPkt_%(name)s' % pktDef)

def getFvwmPktObj(pktType, pktLen = -1):
    pktDict = PacketTypes[pktType]
    if pktLen >= 0 and pktDict['type'] == PKT_TYPE_DYNAMIC:
        # Calculate the packet base size if needed...
        if not pktDict.has_key('baseSize'):
            resizeable = pktDict['fields'][-1]
            pktDict['fields'] = pktDict['fields'][:-1]
            __createCtypeStruct(pktDict)
            pktDict['fields'].append(resizeable)
            pktDict['baseSize'] = len(pktDict['class']())

        # Calculate the packet current size...
        pktDict['fields'][-1] = (pktDict['fields'][-1][0],
                                 'ctypes.c_char * %i' % (pktLen - pktDict['baseSize']))

        # Crete the new class
        __createCtypeStruct(pktDict)

    elif not pktDict.has_key('class') and pktDict['type'] in (PKT_TYPE_STATIC, PKT_TYPE_DYNAMIC):
        __createCtypeStruct(pktDict)

    elif not pktDict.has_key('class') and pktDict['type'] == PKT_TYPE_SWIG:
        __createSwigStrict(pktDict)

    # Create the object and return it
    return pktDict['class']()

if __name__ == '__main__':
    testData = '\xff\xff\xff\xff\x04\x00\x00\x80\x07\x00\x00\x00l\xdc\xf5\x05'
    pkt = FvwmPktHeader()
    pkt.data = ctypes.create_string_buffer(testData,len(testData))
    #print  pkt.type == 0x80000004, pkt.raw_length == 0x00000007
    print pkt.data == testData, pkt.type == 0x80000004, pkt.raw_length == 0x00000007
    print repr(testData)
    print repr(pkt.data)
    print "%08X"%pkt.type, "%08X"%0x80000004
    print pkt.raw_length, 0x00000007

# vim:set tw=180 ts=4 sw=4 et nu:
