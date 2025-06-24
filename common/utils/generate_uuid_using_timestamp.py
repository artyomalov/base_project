from time import time
from uuid import uuid4


def generate_uuid_using_uuid_and_time() -> str:
    random_timestamp = str(time() * 1000).split(".")[0]
    return str(uuid4()) + random_timestamp
