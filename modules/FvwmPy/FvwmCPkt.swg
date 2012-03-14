%module FvwmCPkt
%{
#define class xhint_class
#include "fvwm/fvwm.h"
#include "libs/Module.h"
#include "libs/vpacket.h"

%}

// Ignore all functions, we do not ahve them available in Python!
%ignore SetMWM_INFO;
%ignore fvmm_deinstall_signals;
%ignore SendText;
%ignore ReadFvwmPacket;
%ignore SendFinishedStartupNotification;
%ignore SendUnlockNotification;
%ignore SendQuitNotification;
%ignore SendFvwmPipe;
%ignore SetMessageMask;
%ignore SetSyncMask;
%ignore SetNoGrabMask;
%ignore InitGetConfigLine;
%ignore GetConfigLine;
%ignore module_expand_action;
%ignore ParseModuleArgs;

// #define constants are normally converted to signed integers,
// but some should be treated as unsigned integers....
%typemap(constcode,noblock=1) int MX_VISIBLE_ICON_NAME,
                              int MX_ENTER_WINDOW,
                              int MX_LEAVE_WINDOW,
                              int MX_PROPERTY_CHANGE,
                              int MX_REPLY,
                              int START_FLAG
{
  %set_constant("$symname", PyLong_FromUnsignedLong($value));
}

%typemap(in) (char *rawDataSet, size_t rawDataLen) {
  if (!PyString_Check($input)) {
    PyErr_SetString(PyExc_ValueError, "Expecting a string");
    return NULL;
  }
  $1 = PyString_AsString($input);   /* char* data */
  $2 = PyString_Size($input);       /* int dataLen   */
}

%typemap(in,numinputs=0) char** rawDataGet(char* temp) {
    $1 = &temp;
}

// Return the buffer.  Discarding any previous return result
%typemap(argout) char **rawDataGet {
   Py_XDECREF($result);   /* Blow away any previous result */
   $result = PyString_FromStringAndSize(*$1,result);
   free(*$1);
}

// rename stuff to avoid problems....
%rename(xhint_class) class;

// Include the header files with information that should be available in
// Python code....
%include "fvwm/fvwm.h"
%include "libs/vpacket.h"
%include "libs/Module.h"


// Extend the C data structures to provide utility functions in Python

%extend ConfigWinPacket
{
  int __len__()
  {
    return sizeof(ConfigWinPacket);
  }

  void __setData(char* rawDataSet, size_t rawDataLen)
  {
    memcpy($self, rawDataSet, (rawDataLen < sizeof(ConfigWinPacket) ? rawDataLen : sizeof(ConfigWinPacket)));
  }

  int __getData(char** rawDataGet)
  {
    *rawDataGet=malloc(sizeof(ConfigWinPacket));
    memcpy(*rawDataGet, $self, sizeof(ConfigWinPacket));
    return sizeof(ConfigWinPacket);
  }
};

%extend MiniIconPacket
{
  int __len__()
  {
    return sizeof(MiniIconPacket);
  }

  void __setData(char* rawDataSet, size_t rawDataLen)
  {
    memcpy($self, rawDataSet, (rawDataLen < sizeof(MiniIconPacket) ? rawDataLen : sizeof(MiniIconPacket)));
  }

  int __getData(char** rawDataGet)
  {
    *rawDataGet=malloc(sizeof(MiniIconPacket));
    memcpy(*rawDataGet, $self, sizeof(MiniIconPacket));
    return sizeof(MiniIconPacket);
  }
};

/* vim:set nu et ft=cpp ts=2 sw=2 cino=>2 fo=croq: */
