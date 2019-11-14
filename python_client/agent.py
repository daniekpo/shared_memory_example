import numpy as np
import shmem

class MyAppAgent:
    def __init__(self, client):
        self.name = "android"
        self._client = client
        self._num_control_schemes = 4
        self._control_scheme_buffer = self._client.malloc("shared_buffer_name", [1], np.uint8)
        self.set_control_scheme(3)

    def set_control_scheme(self, index):
        self._current_control_scheme = index % self._num_control_schemes
        self._control_scheme_buffer[0] = self._current_control_scheme

    def get_control_scheme(self):
        return self._control_scheme_buffer[0]
