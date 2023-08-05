from .execution import Executor
from .client import Ingester, Reader
from .const import DEFAULT_HOST, ResourceTypes, FieldTypes


class SimpleClient:

    def __init__(self, apikey, host=DEFAULT_HOST):
        self.apikey = apikey
        self.host = host
        self.exc = Executor(apikey, host)
        self.ig = Ingester(apikey, host)
        self.reader = Reader(apikey, host)

    def create_stream(self, name):
        self.exc.register_stream(name).commit()

    def delete_stream(self, name):
        self.exc.deregister_stream(name)

    def create_lookup(self, name):
        self.exc.register_lookup(name).commit()
        return self.exc.register_transformation(name).sink(name, ResourceTypes.Lookup)

    def delete_lookup(self, name):
        self.exc.deregister_lookup(name)
        self.exc.deregister_transformation(name)

    def lookup(self, table, key=None):
        return self.reader.lookup(table, key)

    def list_resources(self):
        return self.exc.get_resources()

    def list_transforms(self):
        return self.exc.get_transformations()

    def get_transform_status(self, name):
        return self.exc.get_transformation_status(name)

    def send(self, stream, data):
        self.ig.put(stream, data)

    def subscribe(self, transform, callback):
        self.reader.subscribe(transform, callback)

    def unsubscribe(self, transform):
        self.reader.unsubscribe(transform)


ResourceTypes = ResourceTypes
FieldTypes = FieldTypes
