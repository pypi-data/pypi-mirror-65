from .execution import Executor
from .client import Reader, Ingester

Stream = "STREAM_RESOURCE"
Lookup = "LOOKUP_RESOURCE"

class Connection:
    def __init__(self, apikey, host):
        self.apikey = apikey
        self.host = host

    def execute(self):
        return Executor(self.apikey, self.host)

    def ingest(self):
        return Ingester(self.apikey, self.host)

    def read(self):
        return Reader(self.apikey, self.host)


