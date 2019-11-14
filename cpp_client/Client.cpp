#include "Client.h"
#include <semaphore.h>

using namespace std;

Client::Client(){
    this->uuid = APP_NAME_UUID;
}

Client::~Client() {
    this->kill();
}

void Client::start() {
    serverSemaphore = sem_open(SERVER_SEMAPHORE_PATH, 0);
    clientSemaphore = sem_open(CLIENT_SEMAPHORE_PATH, 0);
}

void Client::kill() {
    memory.clear();
    sem_unlink(SERVER_SEMAPHORE_PATH);
    sem_unlink(CLIENT_SEMAPHORE_PATH);
}

void* Client::malloc(const string &key, unsigned int bufferSize) {
    if (!memory.count(key) || memory[key]->getSize() != bufferSize) {
        memory[key] = unique_ptr<SharedMemory>(new SharedMemory(key, bufferSize));
    }
    return memory[key]->getPtr();
}

void Client::acquire() {
    sem_wait(clientSemaphore);
}

void Client::release() {
    sem_post(serverSemaphore);
}