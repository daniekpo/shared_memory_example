CC = g++
NAME = main
CPP_FILES = main.cpp Server.cpp SharedMemory.cpp
OBJ_FILES = main.o Server.o SharedMemory.o

run: build
	./$(NAME)

build: obj
	$(CC) -g $(OBJ_FILES) -o $(NAME)  -lpthread -lrt

obj: $(CPP_FILES)
	$(CC) -c -g $(CPP_FILES)

clean:
	rm -r $(NAME)
	rm -f *.o