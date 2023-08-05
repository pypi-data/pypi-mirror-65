from plyer import notification
from datetime import datetime
from datetime import timedelta
from dateutil import parser

FMT_DATE = "{:%Y-%m-%d}"
FMT_DATETIME = "{:%Y-%m-%d %H:%M}"


class Date(datetime):
    def std_weekday(self):
        """
        Sunday = 1
        Saturday = 7

        """
        d = self.weekday() + 2
        if d == 8:
            return 1
        return d

    @classmethod
    def current(cls, date=None):
        if not date:
            return Date.from_datetime(datetime.now())
        if isinstance(date, str):
            return Date.from_datetime(parser.parse(date))
        raise Exception("Invalid date input!")

    @classmethod
    def from_datetime(cls, dt):
        return Date(
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond
        )

    def to_datetime(self):
        return datetime(
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second,
            self.microsecond,
        )

    @classmethod
    def parse(cls, datestr):
        if not datestr:
            return None
        return Date.from_datetime(parser.parse(datestr))

    def format(self, format_str=None):
        fmt = format_str if format_str else FMT_DATETIME
        return self.strftime(fmt)

    def days_to_end_of_week(self):
        week_day = self.std_weekday()
        return 7 - week_day

    def days_from_start_of_week(self):
        return self.std_weekday() - 1

    def start_of_week(self):
        """
        This will return the preceeding Sunday at 12:00:00 am.

        """
        bow = self - timedelta(days=self.days_from_start_of_week())
        return self.from_datetime(bow).start_of_day()

    def end_of_week(self):
        """
        This will return the following Sunday at 12:00:00 am.

        """
        eow = self + timedelta(days=self.days_to_end_of_week() + 1)
        return self.from_datetime(eow).start_of_day()

    def start_of_day(self, hour=0, minute=0):
        return self.replace(hour=hour, minute=minute, second=0, microsecond=0)

    def next_day(self):
        return Date(self.to_datetime() + timedelta(day=1)).start_of_day()


class StopWatch:

    def __init__(self):
        self.start_time = None
        self.stop_time = None
        self.duration = 0
        self.alerts = []

    def start(self):
        self.start_time = datetime.now()

    def stop(self):
        self.stop_time = datetime.now()

    def reset(self):
        self.start()


class Alarm:

    def __init__(self, entry, alarms):
        self.entry = entry
        self.alarms = alarms[:]

    def __call__(self):
        # TODO: notify is blocking, so it freezes the program
        # until the timeout expires, which fucks everything.
        # Would need to do something to be able to shut down
        # the thread to make this useful.
        return
        #  notification.notify(
        #      title=f"{self.entry.category.name}",
        #      message=f"Timer Entry for {self.entry.project.name} is still running...",
        #      app_name="TTMR",
        #      timeout=60
        #  )


class Timer:
    def __init__(self, start_time, alarm=None):
        if isinstance(start_time, datetime):
            self.start_time = start_time
        elif isinstance(start_time, str):
            self.start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        else:
            self.start_time = start_time

        self.alarm = alarm

    def check_alarms(self):
        if not self.alarm:
            return
        total_minutes = self.get_lapsed_minutes()
        for i in range(0, len(self.alarm.alarms)):
            minute = self.alarm.alarms[i]
            #  print(f"{minute} >= {total_minutes} ???")
            if minute <= total_minutes:
                self.alarm.alarms.pop(i)
                self.alarm()
                return

    def get_lapsed_seconds(self):
        end_time = datetime.now()
        duration = end_time - self.start_time
        return duration.total_seconds()

    def get_lapsed_minutes(self):
        return int(self.get_lapsed_seconds() / 60)

    def get_formatted_lapsed_time(self):
        total_seconds = self.get_lapsed_seconds()
        seconds = int(total_seconds) % 60
        total_minutes = int(total_seconds) / 60
        minutes = int(total_minutes % 60)
        hours = int(int(total_minutes) / 60)
        return "{:0>2}:{:0>2}:{:0>2}".format(hours, minutes, seconds)
