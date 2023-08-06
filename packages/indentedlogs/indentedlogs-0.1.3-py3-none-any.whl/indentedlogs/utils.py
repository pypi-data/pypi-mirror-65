import gc
import inspect
from typing import Callable


def func_in_frame_info(frame_info: inspect.FrameInfo) -> Callable:
    """Find callable corresponding to given frame_info."""
    f_code = frame_info.frame.f_code
    for obj in gc.get_referrers(f_code):
        if hasattr(obj, '__code__') and obj.__code__ is f_code:
            return obj
    raise RuntimeError("Callable not found")
