import time
from typing import Literal


def sync_function(arg: float, origin: Literal['A', 'T', 'P']):
    print(origin, arg, 'Sync Function')
    time.sleep(1)
