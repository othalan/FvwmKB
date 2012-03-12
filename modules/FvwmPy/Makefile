FVWM_SRC_DIR = ${HOME}/src/fvwm-2.5.30.ds
SRCS  = $(wildcard *.swg)
CSRCS = $(SRCS:%.swg=%_wrap.c)
PYS   = $(SRCS:%.swg=%.py)

CFLAGS   = $(shell python2.7-config --cflags)
CFLAGS  += -I${FVWM_SRC_DIR} -I${FVWM_SRC_DIR}/fvwm
CFLAGS  += $(shell freetype-config --cflags)

LDFLAGS  = $(shell python2.7-config --ldflags)

.PHONY: all
all: _FvwmPkt.so

FvwmPkt_wrap.c: fvwm_mod.h fvwm_extension.h

_FvwmPkt.so: FvwmPkt_wrap.o
	gcc -shared $(LDFLAGS) $^ -o $@

# The fvwm main include file needs to be modified before it can be used in
# Python via a SWIG interface because of the following problems:
# - Function declaration SetMWM_INFO must be removed
# - Function declaration fvmm_deinstall_signals must be removed
fvwm_mod.h: ${FVWM_SRC_DIR}/fvwm/fvwm.h Makefile
	sed     's/^.*SetMWM_INFO.*// ' $< \
	  | sed 's/^.*fvmm_deinstall_signals.*// ' \
      > $@

%_wrap.c: %.swg
	swig -w301 -python -I${FVWM_SRC_DIR} -o $@ $<

%.o: %.cpp
	g++ -fPIC -c ${CFLAGS} $< -o $@

%.o: %.c
	gcc -fPIC -c ${CFLAGS} $< -o $@

clean:
	rm -f *.pyc
	rm -f $(OBJS)
	rm -f $(CSRCS)
	rm -f $(PYS)
	rm -f fvwm_mod.h
	rm -f *.so
	rm -f *.o
	rm -f *_wrap.cpp
	rm -f *_wrap.c
