import os
import time
from random import randint
from meross_iot.manager import MerossManager
from timeit import default_timer as timer


EMAIL ="albertogeniola@gmail.com"
PASSWORD ="ciaociao"

script_start = timer()
manager = MerossManager(meross_email=EMAIL, meross_password=PASSWORD)
manager_created = timer()
manager.start()
manager_started = timer()
channel_operation = timer()
manager.stop()
manager_stopped = timer()

print(f"Total execution time {manager_stopped - script_start}")
print(f"- Manager creation: {manager_created - script_start}")
print(f"- Manager initialization: {manager_started - manager_created}")

print(f"- Manager stop: {manager_stopped - channel_operation}")