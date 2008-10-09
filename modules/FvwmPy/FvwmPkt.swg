%module FvwmPkt
%{
#define class xhint_class
#include "fvwm_mod.h"
#include "libs/vpacket.h"
%}

%rename(xhint_class) class;
%include "fvwm_mod.h"
%include "libs/vpacket.h"
