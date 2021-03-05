from sqlalchemy import Column, ForeignKey, MetaData
from sqlalchemy import BigInteger, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import JSONB


from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime, timedelta
import pytz


meta = MetaData(  # automatically name constraints to simplify migrations
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
Base = declarative_base(metadata=meta)


def local_time() -> datetime:
    """ time in Ukraine """
    kiev_tz = pytz.timezone("Europe/Kiev")
    current_time = datetime.now(tz=kiev_tz)
    return current_time


class University(Base):
    __tablename__ = "university"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    students_number = Column(Integer)
    engine_name = Column(String(25))
    engine_parameters = Column(JSONB)
    structure = Column(JSONB)

    def __repr__(self):
        return "<University(id='{}', name='{}', students_number='{}')>".format(
            self.id,
            self.name,
            self.students_number,
        )


class User(Base):
    __tablename__ = "user"

    chat_id = Column(BigInteger, primary_key=True)
    is_banned = Column(Boolean)
    is_group = Column(Boolean)
    username = Column(String(35))  # Telegram allows username no longer then 32
    first_name = Column(String)  # first name is unlimited
    university_id = Column(Integer, ForeignKey("university.id"))
    user_data = Column(JSONB)
    time_registered = Column(DateTime(timezone=True), default=local_time)

    university = relationship(
        "University", backref="university", foreign_keys=[university_id]
    )

    def __repr__(self):
        return "<User(chat_id='{}', username='{}', university='{}')>".format(
            self.chat_id, self.username, self.university_id
        )


class Group(Base):
    __tablename__ = "group"

    chat_id = Column(BigInteger, ForeignKey("user.chat_id"), primary_key=True)
    members_count = Column(Integer)

    user = relationship("User", backref="group", foreign_keys=[chat_id])

    def __repr__(self):
        return "<Group(chat_id='{}', members_count='{}')>".format(
            self.chat_id, self.members_count
        )


class UserAction(Base):
    __tablename__ = "user_action"

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, ForeignKey("user.chat_id"))
    action = Column(Integer, ForeignKey("action.id"))
    time_clicked = Column(DateTime(timezone=True), default=local_time)

    user = relationship("User", backref="user_action", foreign_keys=[chat_id])
    action_name = relationship(
        "Action", backref="user_action_name", foreign_keys=[action]
    )

    def __repr__(self):
        return "<Action(id='{}', chat_id='{}', action='{}', time='{}')>".format(
            self.id, self.chat_id, self.action, self.time_clicked
        )


class Action(Base):
    __tablename__ = "action"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<ActionType(id='{}', name='{}')>".format(self.id, self.name)


class Timer(Base):
    __tablename__ = "timer"

    chat_id = Column(BigInteger, ForeignKey("user.chat_id"), primary_key=True)
    hour = Column(Integer)

    user = relationship("User", backref="timer", foreign_keys=[chat_id])

    def __repr__(self):
        return "<Timer(chat_id='%s', hour='%s')>".format(self.chat_id, self.hour)
