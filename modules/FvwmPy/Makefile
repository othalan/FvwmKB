FVWM_SRC_DIR = ${HOME}/src/fvwm-2.5.30.ds
SRCS  = $(wildcard *.swg)
CSRCS = $(SRCS:%.swg=%_wrap.c)
PYS   = $(SRCS:%.swg=%.py)

CFLAGS   = $(shell python2.7-config --cflags)
CFLAGS  += -I${FVWM_SRC_DIR} -I${FVWM_SRC_DIR}/fvwm
CFLAGS  += $(shell freetype-config --cflags)

LDFLAGS  = $(shell python2.7-config --ldflags)

.PHONY: all
all: _FvwmCPkt.so

FvwmCPkt_wrap.c: fvwm_extension.h

_%.so: %_wrap.o
	gcc -shared $(LDFLAGS) $^ -o $@

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
	rm -f *.so
	rm -f *.o
	rm -f *_wrap.cpp
	rm -f *_wrap.c
