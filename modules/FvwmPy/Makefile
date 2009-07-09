FVWM_SRC_DIR = ${HOME}/src/fvwm-2.5.26
SRCS  = $(wildcard *.swg)
CSRCS = $(SRCS:%.swg=%_wrap.cpp)
PYS   = $(SRCS:%.swg=%.py)

CFLAGS   = $(shell python2.5-config --cflags)
CFLAGS  += -I${FVWM_SRC_DIR} -I${FVWM_SRC_DIR}/fvwm
CFLAGS  += $(shell freetype-config --cflags)

LDFLAGS  = $(shell python2.5-config --ldflags)

.PHONY: all
all: _FvwmPkt.so

FvwmPkt_wrap.cpp: fvwm_mod.h fvwm_extension.h

_FvwmPkt.so: FvwmPkt_wrap.o
	g++ -shared $(LDFLAGS) $^ -o $@

fvwm_mod.h: ${FVWM_SRC_DIR}/fvwm/fvwm.h
	sed     's/\(\<icon_boxes\>\)\([^;]\)/\1_type\2/' $< \
	  | sed 's/\(} *\)\(\<icon_boxes\>\)/\1\2_type/' \
	  | sed 's/^.*SetMWM_INFO.*//' > $@

%_wrap.cpp: %.swg
	swig -python -I${FVWM_SRC_DIR} -o $@ $<

%.o: %.cpp
	g++ -fPIC -c ${CFLAGS} $< -o $@


clean:
	rm -f *.pyc
	rm -f $(OBJS)
	rm -f $(CSRCS)
	rm -f $(PYS)
	rm -f fvwm_mod.h
	rm -f *.so
	rm -f *.o
	rm -f *_wrap.cpp
