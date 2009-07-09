/* Purpose: FVWM SWIG Extensions
 */
#ifndef __FVWM_SWIG_EXTENSIONS_H__
#define __FVWM_SWIG_EXTENSIONS_H__

#include "fvwm_mod.h"
#include "libs/vpacket.h"

typedef union
{
  char            data[sizeof(ConfigWinPacket)];
  ConfigWinPacket packet;
} ConfigWinPacketUnion;

const unsigned int ConfigWinPacketSize = sizeof(ConfigWinPacket);

typedef union
{
  char           data[sizeof(MiniIconPacket)];
  MiniIconPacket packet;
} MiniIconPacketUnion;

const unsigned int MiniIconPacketSize = sizeof(MiniIconPacket);

#endif // __FVWM_SWIG_EXTENSIONS_H__
