%module FvwmPkt
%{
#define class xhint_class
#include "fvwm_mod.h"
#include "libs/vpacket.h"
#include "fvwm_extension.h"

%}

%rename(xhint_class) class;
%include "fvwm_mod.h"
%include "libs/vpacket.h"
%include "fvwm_extension.h"

/* vim:set nu et ft=cpp ts=2 sw=2 cino=>2 fo=croq: */
