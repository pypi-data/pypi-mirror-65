import os
import platform
import subprocess
from contextlib import contextmanager
from functools import wraps
from ..database import init


@contextmanager
def new_session(db_pth):
    Session = init(db_pth)
    db = Session()
    try:
        yield db
    finally:
        db.close()


def db_session(func):
    @wraps(func)
    def _db_session(cfg, *args, **kwargs):
        with new_session(cfg.db_path) as db:
            cfg.db = db
            return func(cfg, *args, **kwargs)

    return _db_session


def open_file(filepath):
    if platform.system() == "Windows":
        os.startfile(filepath)  # pylint: disable=E1101
    elif platform.system() == "Darmin":
        subprocess.Popen(["open", filepath])
    else:
        subprocess.Popen(["xdg-open", filepath])
