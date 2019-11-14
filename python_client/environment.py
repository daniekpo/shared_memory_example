from client import MyAppClient
from agent import MyAppAgent


class MyAppEnvironment:
    """
    Proxy for communicating with MyApp world
    """
    def __init__(self):
        self._client = MyAppClient()
        self._agents = dict()
        self._agent = None
        self._num_agents = 1
        self.add_agent()

        self._client.acquire()


    def add_agent(self):
        agent = MyAppAgent(self._client)
        self._agents[agent.name] = agent
        self._agent = agent


    def tick(self, num_ticks = 1):
        for _ in range(num_ticks):
            self._client.release()
            self._client.acquire()
        
        return self._agent.get_control_scheme()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._client.unlink()


