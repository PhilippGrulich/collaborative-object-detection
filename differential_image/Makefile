#
# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

HOST_SYSTEM = $(shell uname | cut -f 1 -d_)
SYSTEM ?= $(HOST_SYSTEM)
CXX = g++ -Ofast
CPPFLAGS += `pkg-config --cflags opencv`
CXXFLAGS += -std=c++11
ifeq ($(SYSTEM),Darwin)
LDFLAGS += -L/usr/local/lib `pkg-config --libs opencv` \
           -lgrpc++_reflection\
           -ldl
else
LDFLAGS += -L/usr/local/lib  `pkg-config --libs opencv`  \
           -Wl,--no-as-needed -Wl,--as-needed\
           -ldl -pthread
endif


all: main

main: main.o
	$(CXX) $^ $(LDFLAGS) -o diff_image

clean:
	rm -f *.o diff_image

