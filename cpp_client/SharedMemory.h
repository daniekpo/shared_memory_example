#ifndef SHARED_MEMORY_H
#define SHARED_MEMORY_H

#include <iostream>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>

using namespace std;

class SharedMemory
{
private:
    string memPath;
    unsigned int memSize;
	void* memPointer;
    int memFile;

public:
    explicit SharedMemory(const string& name, unsigned int bufferSize);
    ~SharedMemory();

    void* getPtr() const {return memPointer;}
    int getSize() const {return memSize;}
};


#endif
