from datetime import datetime
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from ttmr.time import Date


Base = declarative_base()


def init(dbfile):
    engine = create_engine(f"sqlite:///{dbfile}")
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)


class BaseTable:  # pylint: disable=R0903
    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean(), default=True)
    created = Column(DateTime(timezone=False), default=datetime.now)
    modified = Column(
        DateTime(timezone=False), default=datetime.now, onupdate=datetime.now
    )

    @classmethod
    def get_all(cls, db):
        return db.query(cls).all()

    @classmethod
    def get_active(cls, db):
        # pylint: disable=C0121
        return db.query(cls).filter(cls.active == True).all()  # noqa


FMTS = {
    "INC": "{}{:0>8}",
    "WO": "{}{:0>9}",
    "FY16": "{}-{:0>6}",
    "FY17": "{}-{:0>6}",
    "FY18": "{}-{:0>6}",
    "FY19": "{}-{:0>6}",
    "FY20": "{}-{:0>6}",
    "FY21": "{}-{:0>6}",
    "FY22": "{}-{:0>6}",
    "": "{}-{:0>8}",
}


class Project(Base, BaseTable):
    __tablename__ = "project"

    type = Column(String(25), nullable=False)
    number = Column(Integer, nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    persistant = Column(Boolean(), default=False)

    @property
    def identifier(self):
        return FMTS.get(self.type, FMTS[""]).format(self.type, self.number)


class Category(Base, BaseTable):
    __tablename__ = "category"
    name = Column(String(100), nullable=False, unique=True)


class Entry(Base, BaseTable):
    __tablename__ = "entry"
    category_id = Column(Integer, ForeignKey(Category.id))
    category = relationship(Category, lazy="immediate")
    project_id = Column(Integer, ForeignKey(Project.id))
    project = relationship(Project)
    note = Column(Text, default="")
    start_time = Column(DateTime(timezone=False), unique=True)
    end_time = Column(DateTime(timezone=False), unique=True)
    duration = Column(Integer)

    @property
    def is_completed(self):
        return self.end_time and self.end_time

    @property
    def minutes(self):
        return self.duration

    @property
    def hours(self):
        return round((self.duration / 60.0), 2)

    def start(self):
        self.start_time = Date.current()

    def end(self, end_time=None):
        if not self.start_time:
            raise Exception("You cannot end an entry without a start time.")
        if end_time:
            self.end_time = end_time
        else:
            self.end_time = Date.current()
        self.duration = self.calculate_duration()

    def calculate_duration(self):
        if not self.end_time or not self.end_time:
            raise Exception("You cannot end an entry without a start time.")

        elapsed_time = self.end_time - self.start_time
        return int(elapsed_time.total_seconds() / 60)

    def reset_duration(self):
        self.duration = self.calculate_duration()

    def __str__(self):
        return (
            f"   Category: {self.category.name}\n"
            f"   Incident: {self.project.name}\n"
            f"       Note: {self.note}\n"
            f" Start time: {self.start_time}\n"
            f"   End time: {self.end_time}\n"
            f"   Duration: {self.minutes}\n"
        )

    @classmethod
    def get_day_start_entry(cls, hour=7, minute=0):
        entry = cls(note="start of day")
        entry.start_time = end_time = Date.current().start_of_day(hour=hour, minute=minute)
        entry.end_time = end_time
        entry.duration = 0
        return entry

    @classmethod
    def get_last(cls, db, given_datetime):
        day = given_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        query = db.query(cls).filter(cls.start_time >= day)
        query = query.order_by(desc(cls.start_time))
        return query.first()

    @classmethod
    def all_between(cls, db, start_date, end_date):
        qry = db.query(Entry)
        if start_date:
            qry = qry.filter(Entry.start_time>= start_date.start_of_day())
        if end_date:
            qry = qry.filter(Entry.end_time <= end_date.next_day())
        qry = qry.order_by(Entry.start_time)
        return qry.all()

    @classmethod
    def current_week(cls, db, today=None):
        if not today:
            today = Date.current(date=today).start_of_week()
        bow = today.get_start_of_week()
        print(f"start of week: {bow}")
        query = db.query(cls).filter(cls.start_time >= bow)
        query = query.order_by(cls.start_time)
        return query.all()

    @classmethod
    def day_summary(cls, db, today=None):
        if not today:
            today = Date.current(date=today).start_of_day()
        query = db.query(
            func.min(cls.start_time),
            func.min(cls.start_time),
            func.max(cls.end_time),
            func.sum(cls.duration),
            (func.sum(cls.duration) / 60.0),
        )
        query = query.filter(cls.start_time >= today)
        return query.all()

    @classmethod
    def week_summary(cls, db, today=None):
        if not today:
            today = Date.current(date=today).get_start_of_week()
        query = db.query(Category.name, func.count(cls.id), func.sum(cls.duration))
        query = query.filter(cls.start_time >= today)
        return query.group_by(Category.name).all()
