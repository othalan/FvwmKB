%module FvwmCPkt
%{
#define class xhint_class
#include "fvwm/fvwm.h"
#include "libs/Module.h"
#include "libs/vpacket.h"
#include "fvwm/focus_policy.h"

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
%ignore fpol_init_default_fp;
%ignore fpol_query_allow_set_focus;
%ignore fpol_query_allow_user_focus;
%ignore fpol_is_policy_changed;

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

// Raw data get/set methods need different C and Python behavior for the
// function calls.  The  following typemaps make everything behave as
// expected/needed in each scenario.

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
%include "fvwm/focus_policy.h"

// Extend the C data structures to provide utility functions in Python
// This adds the following features:
// - Allow the length of a structre to be determined auto-magically
// - Allow raw data get/set
// NOTE:  This is typically only useful in Python for a top-level
//        structure.  Any structures within structures are typically only
//        accessed indirectly for this functionality (through the parent).

#define EXTEND_C_PKT(struct_name) \
%extend struct_name \
{ \
  int __len__() \
  { \
    return sizeof(struct_name); \
  } \
 \
  void _setData(char* rawDataSet, size_t rawDataLen) \
  { \
    memcpy($self, rawDataSet, (rawDataLen < sizeof(struct_name) ? rawDataLen : sizeof(struct_name))); \
  } \
 \
  int _getData(char** rawDataGet) \
  { \
    *rawDataGet=malloc(sizeof(struct_name)); \
    memcpy(*rawDataGet, $self, sizeof(struct_name)); \
    return sizeof(struct_name); \
  } \
};

EXTEND_C_PKT(ConfigWinPacket)
EXTEND_C_PKT(MiniIconPacket)

/* vim:set nu et ft=cpp ts=2 sw=2 cino=>2 fo=croq: */
