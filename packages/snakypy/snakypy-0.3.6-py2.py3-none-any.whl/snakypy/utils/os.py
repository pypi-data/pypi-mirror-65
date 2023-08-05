import os


def rmdir_blank(path):
    """Removes folders recursively if they are empty from a
    certain path."""
    for r, d, f in os.walk(path, topdown=False):
        for folder in d:
            if len(os.listdir(os.path.join(r, folder))) == 0:
                try:
                    os.rmdir(os.path.join(r, folder))
                except PermissionError:
                    raise PermissionError("No permission to remove empty folders")
                except Exception:
                    raise Exception("It was not possible to clean empty folders.")
