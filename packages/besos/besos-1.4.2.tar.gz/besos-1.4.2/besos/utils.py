import tempfile
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def create_temp_directory():
    """ Creates a temporary directory.
        The directory will automatically get deleted when leaving the context."""
    tempdir = tempfile.TemporaryDirectory()
    path = tempdir.name
    try:
        yield path
    finally:
        tempdir.cleanup()


def resolve_path(*path):
    if path[0] is None:
        return None
    return str(Path(*path).resolve())
