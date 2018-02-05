OBJS = lib_anneal.o

CPU_CC = g++
CPU_BINDFLAGS = -O3 -Wall -shared -fopenmp -std=c++11 -fPIC `python3 -m pybind11 --includes`

lib_anneal : $(OBJS)
	$(CPU_CC) $(CPU_BINDFLAGS) $(OBJS) -o lib_anneal`python3-config --extension-suffix`

lib_anneal.o: 
	$(CPU_CC) $(CPU_BINDFLAGS) -c lib_anneal.cpp

clean:
	rm *.so *.o *.gch
