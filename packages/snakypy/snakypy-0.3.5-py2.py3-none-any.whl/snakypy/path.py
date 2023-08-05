from pathlib import Path


def create(*args, multidir=()):
    """
    Function that creates single or multiple directories.

    E.g:

    >>> import snakypy
    >>> dirs = ("/tmp/foo/bar", "/tmp/foo/xyz")
    >>> snakypy.path.create("/tmp/bar", "/tmp/bar/foo")
    >>> snakypy.path.create(multidir=dirs)
    >>> snakypy.path.create("/tmp/bar", "/tmp/bar/foo", multidir=dirs)

    Arguments:
        **args {str}** -- You must receive one or more unique arguments.

    Keyword Arguments:
        **multidir {tuple}** -- You should receive a tuple with the paths to be created.
    """
    try:
        # Create directory single.
        if args:
            for directory in args:
                path = Path(directory)
                path.mkdir(parents=True, exist_ok=True)
    except TypeError:
        raise TypeError(
            ">>> Invalid type. You should receive only one argument at a time."
        )
    except Exception:
        raise Exception(f">>> An error occurred while creating directory: {args}")

    try:
        # Create multiple directory.
        if len(multidir) > 0:
            for directory in multidir:
                path = Path(directory)
                path.mkdir(parents=True, exist_ok=True)
    except TypeError:
        raise TypeError(f">>> You should receive a tuple.")
    except Exception:
        raise Exception(f">>> There was an error creating directories: {multidir}")
