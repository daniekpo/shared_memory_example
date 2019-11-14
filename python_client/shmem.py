"""Shared memory with memory mapping"""
import ctypes
import mmap
import os
from functools import reduce

import numpy as np


class Shmem:
    """Implementation of shared memory


    Args:
        name (:obj:`str`): Name the points to the beginning of the shared memory block
        shape (:obj:`int`): Shape of the memory block
        dtype (type, optional): data type of the shared memory. Defaults to np.float32
        uuid (:obj:`str`, optional): UUID of the memory block. Defaults to ""
    """
    _numpy_to_ctype = {
        np.float32: ctypes.c_float,
        np.uint8: ctypes.c_uint8,
        np.bool: ctypes.c_bool,
        np.byte: ctypes.c_byte
    }

    def __init__(self, name, shape, dtype=np.float32, uuid=""):
        self.shape = shape
        self.dtype = dtype
        size = reduce(lambda x, y: x * y, shape)
        size_bytes = np.dtype(dtype).itemsize * size

        self._mem_path = None
        self._mem_pointer = None
        if os.name == "nt":
            self._mem_path = "/APP_NAME_MEM" + uuid + "_" + name
            self._mem_pointer = mmap.mmap(0, size_bytes, self._mem_path)
        elif os.name == "posix":
            self._mem_path = "/dev/shm/shared_buffer"
            f = os.open(self._mem_path, os.O_CREAT | os.O_TRUNC | os.O_RDWR)
            self._mem_file = f
            os.ftruncate(f, size_bytes)
            os.fsync(f)

            self._mem_pointer = mmap.mmap(f, size_bytes)


        self.np_array = np.ndarray(shape, dtype=dtype)
        self.np_array.data = (Shmem._numpy_to_ctype[dtype] * size).from_buffer(self._mem_pointer)

    def unlink(self):
        """unlinks the shared memory"""
        if os.name == "posix":
            self.__linux_unlink__()
        elif os.name == "nt":
            self.__windows_unlink__()


    def __linux_unlink__(self):
        os.close(self._mem_file)
        os.remove(self._mem_path)

    def __windows_unlink__(self):
        pass
