from pathlib import Path
from tempfile import NamedTemporaryFile
import csvy
from tabulate import tabulate
from .. import gui
from ..console import BG_WHITE
from ..console import BLACK
from ..console import Console
from ..database import Category
from ..database import Entry
from ..database import Project
from ..time import FMT_DATETIME
from ..util import add_table_border
from ..util import read_file
from .util import db_session
from .util import open_file


@db_session
def list_categories(conf):

    categories = Category.get_all(conf.db)

    Console.write(BG_WHITE)
    Console.write(BLACK)

    table = tabulate(
        [(c.name, c.active, c.created, c.modified) for c in categories],
        headers=("CATEGORY", "ACTIVE", "CREATED", "MODIFED"),
        numalign="decimal",
    )
    Console.write(add_table_border(table))
    Console.newline()
    Console.clear_formating()


@db_session
def list_projects(conf):
    projects = Project.get_all(conf.db)

    Console.write(BG_WHITE)
    Console.write(BLACK)

    table = tabulate(
        [(c.identifier, c.name, c.active, c.created, c.modified) for c in projects],
        headers=("IDENTIFIER", "NAME", "ACTIVE", "CREATED", "MODIFED"),
        numalign="decimal",
    )
    Console.write(add_table_border(table))
    Console.newline()
    Console.clear_formating()


def _list_entries(list_of_entries):
    entries = [
        (
            e.id,
            e.category.name,
            e.project.identifier,
            e.project.name,
            e.note,
            e.start_time,
            e.end_time,
            e.minutes,
            e.hours,
        )
        for e in list_of_entries
    ]

    total_minutes = int(sum([e[7] for e in entries]))
    total_hours = sum([e[7] for e in entries]) / 60.0

    entries.append(
        (None,"", "", "", "", entries[0][5], entries[-1][6], total_minutes, total_hours)
    )

    headers = (
        "ID",
        "CATEGORY",
        "PROJECT ID",
        "PROJECT NAME",
        "NOTE",
        "START",
        "END",
        "DURATION",
        "HOURS",
    )
    formatters = ("{:0>4}", None, None, None, None, FMT_DATETIME, FMT_DATETIME, "{:}", "{:.3}")

    gui.write_table(entries, headers, formatters)

    entries.insert(0, headers)
    return entries


@db_session
def list_entries(conf):
    _list_entries(Entry.all_between(conf.db, conf.start_date, conf.end_date))


def write_to_csv(conf, data):
    filename = Path(NamedTemporaryFile().name).name
    filepath = Path(conf.user_cache_dir, filename + ".csv")
    with csvy.writer(filepath) as csv:
        csv.writerows(data)
    open_file(filepath)


@db_session
def list_current_weeks_entries(conf):
    entries = _list_entries(Entry.current_week(conf.db))
    if conf.cli_args.get("--csv"):
        write_to_csv(conf, entries)


@db_session
def day_summary(conf):
    """
    Displays a summary of the current days total time.

    """
    rows = Entry.day_summary(conf.db)
    data = gui.write_table(
        rows,
        ("DAY", "START", "END", "MINUTES", "HOURS"),
        ("{:%Y-%m-%d}", "{:%H:%M}", "{:%H:%M}", None, "{:.3}"),
    )

    if conf.cli_args.get("--csv"):
        write_to_csv(conf, data)


@db_session
def weekly_summary(conf):
    sql = read_file("week_summary.sql")
    start = conf.today.start_of_week().to_datetime()
    end = conf.today.end_of_week().to_datetime()

    results_proxy = conf.db.execute(sql, {"start_date": start, "end_date": end})
    results = [row for row in results_proxy]

    totals = (
        "TOTALS",
        sum([r[1] for r in results]),
        sum([r[2] for r in results]),
        sum([r[3] for r in results]),
        sum([r[4] for r in results]),
        sum([r[5] for r in results]),
        sum([r[6] for r in results]),
        sum([r[7] for r in results]),
        sum([r[8] for r in results]),

    )

    results.append(totals)

    data = gui.write_table(
        results,
        ("CATEGORY", "SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT", "TOTAL"),
        (None, None, None, None, None, None, None, None, None),
    )

    if conf.cli_args.get("--csv"):
        write_to_csv(conf, data)
