#include "Server.h"
#include <semaphore.h>

using namespace std;

Server::Server(){
    this->uuid = APP_NAME_UUID;
}

Server::~Server() {
    this->kill();
}

void Server::start() {
    // Unlink existing semaphores
    sem_unlink(SERVER_SEMAPHORE_PATH);
    sem_unlink(CLIENT_SEMAPHORE_PATH);

    serverSemaphore = sem_open(SERVER_SEMAPHORE_PATH, O_CREAT, 0777, 0);
    clientSemaphore = sem_open(CLIENT_SEMAPHORE_PATH, O_CREAT, 0777, 0);
}

void Server::kill() {
    memory.clear();
    sem_unlink(SERVER_SEMAPHORE_PATH);
    sem_unlink(CLIENT_SEMAPHORE_PATH);
}

void* Server::malloc(const string &key, unsigned int bufferSize) {
    if (!memory.count(key) || memory[key]->getSize() != bufferSize) {
        memory[key] = unique_ptr<SharedMemory>(new SharedMemory(key, bufferSize));
    }
    return memory[key]->getPtr();
}

void Server::acquire() {
    sem_wait(serverSemaphore);
}

void Server::release() {
    sem_post(clientSemaphore);
}