%module FvwmCPkt
%{
#define class xhint_class
#include "fvwm/fvwm.h"
#include "libs/Module.h"
#include "libs/vpacket.h"
#include "fvwm_extension.h"

%}

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

%typemap(constcode,noblock=1) int MX_VISIBLE_ICON_NAME,
                              int MX_ENTER_WINDOW,
                              int MX_LEAVE_WINDOW,
                              int MX_PROPERTY_CHANGE,
                              int MX_REPLY,
                              int START_FLAG
{
  %set_constant("$symname", PyLong_FromUnsignedLong($value));
}

%rename(xhint_class) class;
%include "fvwm/fvwm.h"
%include "libs/vpacket.h"
%include "fvwm_extension.h"
%include "libs/Module.h"

/* vim:set nu et ft=cpp ts=2 sw=2 cino=>2 fo=croq: */
