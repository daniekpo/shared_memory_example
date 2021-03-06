#include <iostream>
#include "Server.h"
#include <cstring>
#include "SharedMemory.h"
#include <memory>
#include <sys/mman.h>
#include <unistd.h>
#include <fcntl.h>

using namespace std;

void * allocateSharedMem(const string& name, unsigned int bufferSize, void * buffer) {
    const char *filePath = name.c_str();
    int memFile = shm_open(filePath, O_CREAT | O_RDWR, 0777);
    ftruncate(memFile, bufferSize);
    buffer = mmap(0, bufferSize, PROT_READ | PROT_WRITE, MAP_SHARED, memFile, 0);
    return buffer;
}

int main(int argc, char ** argv) {
    Server server;
    server.start();
    uint8_t num = 0;
    bool initialized = false;

    void *sharedBuffer;

    for (int i = 0; i < 10; ++i) {
        server.release();
        server.acquire();

        if (!initialized) {
            sharedBuffer = server.malloc("shared_buffer", sizeof(uint8_t));
            initialized = true;
        }
        
        uint8_t bufferValue =  *(static_cast<uint8_t*>(sharedBuffer)); 

        num  += 8;
        memcpy(sharedBuffer, &num, sizeof(uint8_t));
        *(static_cast<uint8_t*>(sharedBuffer)) = 64;
    }

    return 0;
}