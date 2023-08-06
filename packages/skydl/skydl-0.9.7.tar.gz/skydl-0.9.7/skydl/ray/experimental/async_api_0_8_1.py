# see: https://github.com/ray-project/ray/blob/releases/0.8.1/python/ray/experimental/async_api.py
# 该文件在0.8.1版本的async_api.py基础上删减了不需要的方法
# Note: asyncio is only compatible with Python 3
import functools
import threading
handler = None
transport = None
protocol = None


class _ThreadSafeProxy:
    """This class is used to create a thread-safe proxy for a given object.
        Every method call will be guarded with a lock.
    Attributes:
        orig_obj (object): the original object.
        lock (threading.Lock): the lock object.
        _wrapper_cache (dict): a cache from original object's methods to
            the proxy methods.
    """

    def __init__(self, orig_obj, lock):
        self.orig_obj = orig_obj
        self.lock = lock
        self._wrapper_cache = {}

    def __getattr__(self, attr):
        orig_attr = getattr(self.orig_obj, attr)
        if not callable(orig_attr):
            # If the original attr is a field, just return it.
            return orig_attr
        else:
            # If the orginal attr is a method,
            # return a wrapper that guards the original method with a lock.
            wrapper = self._wrapper_cache.get(attr)
            if wrapper is None:

                @functools.wraps(orig_attr)
                def _wrapper(*args, **kwargs):
                    with self.lock:
                        return orig_attr(*args, **kwargs)

                self._wrapper_cache[attr] = _wrapper
                wrapper = _wrapper
            return wrapper


def thread_safe_client(client, lock=None):
    """Create a thread-safe proxy which locks every method call
    for the given client.
    Args:
        client: the client object to be guarded.
        lock: the lock object that will be used to lock client's methods.
            If None, a new lock will be used.
    Returns:
        A thread-safe proxy for the given client.
    """
    if lock is None:
        lock = threading.Lock()
    return _ThreadSafeProxy(client, lock)

