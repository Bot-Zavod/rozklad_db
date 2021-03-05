from datetime import datetime, timedelta
import pytz

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

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


def local_time():
    kiev_tz = pytz.timezone("Europe/Kiev")
    current_time = datetime.now(tz=kiev_tz)
    return current_time


class UserType(Base):
    __tablename__ = "user_type"

    id = Column(Integer, primary_key=True)
    type = Column(String)

    user = relationship("User")

    def __repr__(self):
        return "<UserType(id='%s', type='%s')>" % (self.id, self.type)


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    user_type = Column(Integer, ForeignKey("user_type.id"))

    time_created = Column(DateTime(timezone=True), default=local_time)

    type = relationship("UserType", back_populates="user")
    student = relationship("Student", back_populates="user", cascade="all, delete")
    teacher = relationship("Teacher", back_populates="user", cascade="all, delete")
    action = relationship("Action", back_populates="user", cascade="all, delete")
    group = relationship("Group", back_populates="user", cascade="all, delete")
    timer = relationship("Timer", back_populates="user", cascade="all, delete")

    def __repr__(self):
        return "<User(user_id='%s', username='%s', userType='%s')>" % (
            self.user_id,
            self.username,
            self.user_type,
        )


class Group(Base):
    __tablename__ = "group"

    group_id = Column(
        Integer, ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True
    )
    members_count = Column(Integer)

    user = relationship("User", back_populates="group")

    def __repr__(self):
        return "<Group(group_id='%s', members_count='%s')>" % (
            self.group_id,
            self.members_count,
        )


class Student(Base):
    __tablename__ = "student"

    student_id = Column(
        Integer, ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True
    )

    facultyId = Column(Integer)
    facultyName = Column(String)

    course = Column(Integer)

    groupId = Column(Integer)
    groupName = Column(String)

    user = relationship("User", back_populates="student")

    def account(self):
        data = {
            "facultyName": self.facultyName,
            "course": self.course,
            "groupName": self.groupName,
        }
        return data

    def request(self):
        data = {
            "facultyId": self.facultyId,
            "course": self.course,
            "groupId": self.groupId,
        }
        return data

    def __repr__(self):
        return (
            "<Student(student_id='%s', facultyId='%s', course='%s', groupId='%s')>"
            % (self.student_id, self.facultyId, self.course, self.groupId)
        )


class Teacher(Base):
    __tablename__ = "teacher"

    teacher_id = Column(
        Integer, ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True
    )

    departmentId = Column(Integer)
    departmentName = Column(String)

    teacherId = Column(Integer)
    teacherName = Column(String)

    user = relationship("User", back_populates="teacher")

    def account(self):
        data = {"departmentName": self.departmentName, "teacherName": self.teacherName}
        return data

    def request(self):
        data = {"departmentId": self.departmentId, "teacherId": self.teacherId}
        return data

    def __repr__(self):
        return "<Teacher(teacher_id='%s', departmentId='%s', teacherId='%s')>" % (
            self.teacher_id,
            self.departmentId,
            self.teacherId,
        )


class Action(Base):
    __tablename__ = "action"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"))
    action_type = Column(Integer, ForeignKey("action_type.id"))
    comment = Column(String)

    time = Column(DateTime(timezone=True), default=local_time)

    user = relationship("User", back_populates="action")
    type = relationship("ActionType", back_populates="action")

    def __repr__(self):
        return (
            "<Action(id='%s', user_id='%s', action_type='%s', comment='%s', time='%s')>"
            % (self.id, self.user_id, self.action_type, self.comment, self.time)
        )


class ActionType(Base):
    __tablename__ = "action_type"

    id = Column(Integer, primary_key=True)
    type = Column(String)

    action = relationship("Action")

    def __repr__(self):
        return "<ActionType(id='%s', type='%s')>" % (self.id, self.type)


class Schedule(Base):
    __tablename__ = "schedule_chache"

    schedule_id = Column(Integer, primary_key=True)
    date = Column(Integer, primary_key=True)
    schedule_text = Column(String)

    def __repr__(self):
        return "<Schedule(schedule_id='%s', date='%s', schedule_text='%s')>" % (
            self.schedule_id,
            self.date,
            self.schedule_text,
        )


class Timer(Base):
    __tablename__ = "timer"

    id = Column(
        Integer, ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True
    )
    hour = Column(Integer)

    user = relationship("User", back_populates="timer")

    def __repr__(self):
        return "<Timer(id='%s', hour='%s')>" % (self.id, self.hour)
