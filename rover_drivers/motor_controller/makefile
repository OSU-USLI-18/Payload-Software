CC = g++
LIBS = -I/usr/local/include -L/usr/local/lib -lwiringPi
FLAGS = $(LIBS) -Wall
STANDARD = -std=c++11

all: dual_mc33926_rpi.cpp dual_mc33926_rpi.hpp
	$(CC) -o dual_mc33926_rpi dual_mc33926_rpi.cpp $(FLAGS)
clean:
	rm dual_mc33926_rpi
