import os
from functools import wraps


def denying_os(os_name):
    """Decorator to ban an operating system from software through os.name.

    Arguments:
        **os_name** {str} - You must receive the os.name of the operating system to be banned.
                            Windows = nt
                            Linux/Mac OS = posix
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if os.name == os_name:
                msg = f"This software is not compatible with this ({os_name}) operating system."
                raise Exception(msg)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def only_for_linux(func):
    """A decorator to force a function or method to run on Unix systems only."""
    import platform

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not platform.system() == "Linux":
            msg = (
                "Invalid operating system. "
                f'This function "{func.__name__}" is only compatible with '
                "Linux systems."
            )
            raise Exception(msg)
        return func(*args, **kwargs)

    return wrapper


__all__ = ["only_for_linux", "denying_os"]
