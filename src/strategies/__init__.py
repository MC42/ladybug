import time
from src.camera import Camera
import cv2

# https://www.geeksforgeeks.org/decorators-in-python/
# decorator to calculate duration
# taken by any function.


def benchmark_ns(func):
    def inner_stub(*args, **kwargs):
        # storing time before function execution
        begin = time.monotonic_ns()
        func(*args, **kwargs)
        # storing time after function execution
        end = time.monotonic_ns()
        print("Total time taken in : ", func.__name__, end - begin)

    return inner_stub


class FocusStackStrategy:
    def __init__(self, camera_obj, motion_obj):
        self.camera = camera_obj
        self.motion_sys = motion_obj

    def executeStrategy(self) -> list:
        """This will contain a pile of functions that are executed internal to this strategy, or to this directory of strategies to be called for ingest and processing.

        This is imperfect, and not a replacement for the plugin system as intended by Yujie and Ahron in other files (largely in ./utils/*.py)"""
        pass
