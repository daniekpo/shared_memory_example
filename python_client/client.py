from shmem import Shmem
from agent import MyAppAgent

class MyAppClient:
    """MyAppClient for controlling a shared memory session.

    Args:
        uuid (:obj:`str`, optional): A UUID to indicate which server this client is associated with.
            The same UUID should be passed to the world through a command line flag. Defaults to "".
        should_timeout (:obj:`boolean`, optional): If the client should time out after 5s waiting for the engine
    """
    def __init__(self, uuid="unique_id_abcd"):
        self._uuid = uuid

        # Important functions
        self._get_semaphore_fn = None
        self._release_semaphore_fn = None
        self._server_semaphore = None
        self._client_semaphore = None
        self.unlink = None

        self._memory = dict()
        self.init()

    def init(self):
        import posix_ipc
        self._server_semaphore = posix_ipc.Semaphore("/APP_NAME_SEMAPHORE_SERVER")
        self._client_semaphore = posix_ipc.Semaphore("/APP_NAME_SEMAPHORE_CLIENT")

  

        def posix_acquire_semaphore(sem):
            sem.acquire()

        def posix_release_semaphore(sem):
            sem.release()

        def posix_unlink():
            posix_ipc.unlink_semaphore("/APP_NAME_SEMAPHORE_SERVER")
            posix_ipc.unlink_semaphore("/APP_NAME_SEMAPHORE_CLIENT")
            for shmem_block in self._memory.values():
                shmem_block.unlink()

        self._get_semaphore_fn = posix_acquire_semaphore
        self._release_semaphore_fn = posix_release_semaphore
        self.unlink = posix_unlink

    def acquire(self):
        # Used to acquire control. Will wait until the unique_id server has finished its work
        self._get_semaphore_fn(self._client_semaphore)

    def release(self):
        # Used to release contol. Will allow the server to take a step.
        self._release_semaphore_fn(self._server_semaphore)


    def malloc(self, key, shape, dtype):
        """Allocates a block of shared memory, and returns a numpy array whose data corresponds
        with that block.

        Args:
            key (:obj:`str`): The key to identify the block.
            shape (:obj:`list` of :obj:`int`): The shape of the numpy array to allocate.
            dtype (type): The numpy data type (e.g. np.float32).

        Returns:
            :obj:`np.ndarray`: The numpy array that is positioned on the shared memory.
        """
        not_in_map = key not in self._memory

        if not_in_map or self._memory[key].shape != shape or self._memory[key].dtype != dtype:
            self._memory[key] = Shmem(key, shape, dtype, self._uuid)

        return self._memory[key].np_array