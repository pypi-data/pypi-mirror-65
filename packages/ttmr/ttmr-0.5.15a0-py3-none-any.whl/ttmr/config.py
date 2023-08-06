import os
from pathlib import Path
from types import SimpleNamespace
import tomlkit
from appdirs import AppDirs
from .time import Date
from .util import get_value


def assert_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_appdir():
    appdirs = AppDirs("ttmr", "mgemmill")
    user_data_dir = appdirs.user_data_dir
    assert_dir(user_data_dir)
    return user_data_dir


def get_config(args):
    cfg = SimpleNamespace()

    cfg.cli_args = args

    cfg.appdirs = appdirs = AppDirs("ttmr", "mgemmill")
    cfg.user_data_dir = app_dir = appdirs.user_data_dir
    cfg.user_cache_dir = cache_dir = Path(appdirs.user_cache_dir)

    assert_dir(app_dir)
    assert_dir(cache_dir)

    cfg.config_path = Path(app_dir, "ttmr.cfg").resolve()

    cfg.data = data = tomlkit.parse(cfg.config_path.read_text())
    cfg.db_path = Path(app_dir, data["ttmr"]["db"])
    #  cfg.timezone = timezone = data["ttmr"].get("timezone", "America/Vancouver")

    cfg.today = Date.current(args.get("--date"))
    cfg.start_date = Date.parse(args.get("--start-date"))
    cfg.end_date = Date.parse(args.get("--end-date"))
    cfg.entry_id = get_value(args.get('--id'), 0, int)

    hour, minute = [int(s) for s in data["ttmr"].get("start_time", "07:00").split(":")]

    cfg.day_start_time = cfg.today.replace(hour=hour, minute=minute)

    cfg.alarms = data["ttmr"].get("alarms", [30,50,65,75])

    return cfg
