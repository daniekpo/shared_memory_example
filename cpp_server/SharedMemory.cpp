#include "SharedMemory.h"

using namespace std;

SharedMemory::SharedMemory(const string& name, unsigned int bufferSize):
    memPath(name), memSize(bufferSize) {
        // Create or open and existing shared memory object. This makes it so we don't
        // create an actual file but maps it to memory as if it existed
        const char * filePath = memPath.c_str();
        cout << filePath << endl;

        memFile = shm_open(filePath, O_CREAT | O_RDWR, 0777);

        // Enlarge to the actual size. The file size is always 0 bytes before this call
        ftruncate(memFile, this->memSize);

        // Create a memory-mapped file from the file descriptor created with shm_open. I.e map the
        // shared file to memory
        memPointer = mmap(nullptr, this->memSize, PROT_READ | PROT_WRITE, MAP_SHARED, memFile, 0);
}

SharedMemory::~SharedMemory() {
    close(memFile);
}