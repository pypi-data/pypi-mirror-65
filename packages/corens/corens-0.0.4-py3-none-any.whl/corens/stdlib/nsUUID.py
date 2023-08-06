import uuid

def id(ns):
    return str(uuid.uuid4())

_lib = {"/bin/id":id}
