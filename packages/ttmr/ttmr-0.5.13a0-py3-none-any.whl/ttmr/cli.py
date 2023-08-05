"""
 Usage:
     ttmr current
     ttmr start
     ttmr stop
     ttmr insert
     ttmr view
     ttmr summary (--day|--week) [--date=<YYYY-MM-DD>] [--csv]
     ttmr weekly [--csv]
     ttmr new  OBJTYPE
     ttmr list OBJTYPE [--inactive] [--start-date=<YYYY-MM-DD>] [--end-date=<YYYY-MM-DD>]

 Options:
   --day                      Show summary for the day.
   --week                     Show summary for the week.
   --date=<YYYY-MM-DD>        Date that defines the day/week.
   --start-date=<YYYY-MM-DD>  Date that defines the day/week.
   --end-date=<YYYY-MM-DD>    Date that defines the day/week.
   --csv                      Output csv formatted file.
   -h --help                  Show this screen.
   --version                  Show version.

"""
import codecs
import colorama
import docopt
import ttmr.config as config
from ttmr.console import GREEN
from ttmr.console import RED
from ttmr.console import Console
from ttmr.util import replace_bad_char
from . import commands

__author__ = "Mark Gemmill"
__email__ = "mark@markgemmill.com"
__version__ = "0.5.13-alpha"


colorama.init()

codecs.register_error("ttmr", replace_bad_char)


def main_wrapper(func):
    def _wrapper_():
        try:
            title = f" Task Timer v{__version__}"
            underline = "-" * (len(title) - 1)
            Console.init()
            Console.newline()
            Console.write(GREEN)
            Console.write(title)
            Console.newline()
            Console.write(f" {underline}")
            Console.clear_formating()
            Console.newline()
            Console.cursor_up()

            func()

            Console.newline()

        except KeyboardInterrupt:
            Console.clear_formating()
            Console.newline()
            Console.newline()
            Console.write(RED)
            Console.writeline("*** Task has been canceled. ***")
            Console.clear_formating()
            Console.newline()

    return _wrapper_


@main_wrapper
def main():

    args = docopt.docopt(__doc__, version="")
    conf = config.get_config(args)
    conf.cli_args = args

    Console.newline()

    if args["stop"]:
        commands.stop_time_entry(conf)
    elif args["start"]:
        commands.start_time_entry(conf)
    elif args['insert']:
        commands.new_time_entry(conf)
    elif args["current"]:
        commands.show_current_entry(conf)
    elif args["summary"] and args["--day"]:
        commands.day_summary(conf)
    elif args["summary"] and args["--week"]:
        commands.weekly_summary(conf)
    elif args["weekly"]:
        commands.list_current_weeks_entries(conf)
    elif args["new"] and args["OBJTYPE"] in ("entry",):
        commands.new_time_entry(conf)
    elif args["new"] and args["OBJTYPE"] in ("cat", "category"):
        commands.new_category(conf)

    elif args["list"] and args["OBJTYPE"] in ("cat", "category"):
        commands.list_categories(conf)

    elif args["new"] and args["OBJTYPE"] in (
        "prj",
        "proj",
        "inc",
        "project",
        "incident",
    ):
        commands.new_project(conf)

    elif args["list"] and args["OBJTYPE"] in (
        "prj",
        "proj",
        "inc",
        "project",
        "incident",
    ):
        commands.list_projects(conf)

    elif args["list"] and args["OBJTYPE"] in ("ent", "entry"):
        commands.list_entries(conf)

    else:
        print("Unknown command: could not complete your request.")
