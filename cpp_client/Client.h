#ifndef CLIENT_H
#define CLIENT_H

#include "SharedMemory.h"

#include <iostream>
#include <map>
#include <memory>
#include <semaphore.h>
#include <sys/mman.h>
#include <unistd.h>

#define SERVER_SEMAPHORE_PATH "/APP_NAME_SEMAPHORE_SERVER"
#define CLIENT_SEMAPHORE_PATH "/APP_NAME_SEMAPHORE_CLIENT"
#define APP_NAME_UUID "unique_id_abcd"

using namespace std;

class Client
{
private:
    string uuid;
    map<string, unique_ptr<SharedMemory>> memory;
    sem_t* serverSemaphore;
    sem_t* clientSemaphore;

public:
    Client();
    ~Client();

    void start();
    void kill();
    void* malloc(const string &key, unsigned int bufferSize);
    void acquire();
    void release();
};

#endif