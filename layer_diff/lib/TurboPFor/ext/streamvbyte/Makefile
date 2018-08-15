# minimalist makefile
.SUFFIXES:
#
.SUFFIXES: .cpp .o .c .h

PROCESSOR:=$(shell uname -m)

ifeq ($(PROCESSOR), aarch64)
# for 64-bit ARM processors
CFLAGS = -fPIC -std=c99 -O3 -Wall -Wextra -pedantic -Wshadow -D__ARM_NEON__
else ifeq ($(PROCESSOR), armv7l) 
# for 32-bit ARM processors
CFLAGS = -fPIC -std=c99 -O3 -Wall -Wextra -pedantic -Wshadow
else
# Here we expect x64
# Formally speaking, we only need SSE4, at best, but code checks for AVX
# since MSVC only allows to check for AVX and nothing finer like just SSE4
CFLAGS = -fPIC -march=native -std=c99 -O3 -Wall -Wextra -pedantic -Wshadow 
endif
LDFLAGS = -shared
LIBNAME=libstreamvbyte.so.0.0.1
LNLIBNAME=libstreamvbyte.so
all:  unit $(LIBNAME)
test:
	./unit
dyntest:   dynunit $(LNLIBNAME)
	LD_LIBRARY_PATH=. ./dynunit

install: $(OBJECTS) $(LIBNAME)
	cp $(LIBNAME) /usr/local/lib
	ln -f -s /usr/local/lib/$(LIBNAME) /usr/local/lib/libstreamvbyte.so
	ldconfig
	cp $(HEADERS) /usr/local/include



HEADERS=./include/streamvbyte.h ./include/streamvbytedelta.h 

uninstall:
	for h in $(HEADERS) ; do rm  /usr/local/$$h; done
	rm  /usr/local/lib/$(LIBNAME)
	rm /usr/local/lib/libstreamvbyte.so
	ldconfig


OBJECTS= streamvbyte.o streamvbytedelta.o



streamvbytedelta.o: ./src/streamvbytedelta.c $(HEADERS)
	$(CC) $(CFLAGS) -c ./src/streamvbytedelta.c -Iinclude


streamvbyte.o: ./src/streamvbyte.c $(HEADERS)
	$(CC) $(CFLAGS) -c ./src/streamvbyte.c -Iinclude



$(LIBNAME): $(OBJECTS)
	$(CC) $(CFLAGS) -o $(LIBNAME) $(OBJECTS)  $(LDFLAGS)

$(LNLIBNAME): $(LIBNAME)
	ln -f -s $(LIBNAME) $(LNLIBNAME)

shuffle_tables: ./utils/shuffle_tables.c 
	$(CC) $(CFLAGS) -o shuffle_tables ./utils/shuffle_tables.c



example: ./example.c    $(HEADERS) $(OBJECTS)
	$(CC) $(CFLAGS) -o example ./example.c -Iinclude  $(OBJECTS)

perf: ./tests/perf.c    $(HEADERS) $(OBJECTS)
	$(CC) $(CFLAGS) -o perf ./tests/perf.c -Iinclude  $(OBJECTS)

decode_perf: ./tests/decode_perf.c    $(HEADERS) $(OBJECTS)
	$(CC) $(CFLAGS) -o decode_perf ./tests/decode_perf.c -Iinclude  $(OBJECTS)

writeseq: ./tests/writeseq.c    $(HEADERS) $(OBJECTS)
	$(CC) $(CFLAGS) -o writeseq ./tests/writeseq.c -Iinclude  $(OBJECTS)

unit: ./tests/unit.c    $(HEADERS) $(OBJECTS)
	$(CC) $(CFLAGS) -o unit ./tests/unit.c -Iinclude  $(OBJECTS)

dynunit: ./tests/unit.c    $(HEADERS) $(LIBNAME) $(LNLIBNAME)
	$(CC) $(CFLAGS) -o dynunit ./tests/unit.c -Iinclude  -L. -lstreamvbyte

clean:
	rm -f unit *.o $(LIBNAME) $(LNLIBNAME) decode_perf example shuffle_tables perf writeseq dynunit
