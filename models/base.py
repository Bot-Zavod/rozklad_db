from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from os import path, environ
import sys

from sqlalchemy import select
# from progressbar import progressbar


from dotenv import load_dotenv
load_dotenv()

postgres_db = {
    "drivername": "postgres",
    "username": environ["DB_USERNAME"],
    "password": environ["DB_PASSWORD"],
    "host": environ["DB_HOST"],
    "port": int(environ["DB_PORT"]),
    "database": environ["DB_DATABASE"],
}
postgres_uri = URL(**postgres_db)

base_dir = path.dirname(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
sqlite_dir = path.join(base_dir, "new.sqlite")
sqlite_db = {"drivername": "sqlite", "database": sqlite_dir}
sqlite_uri = URL(**sqlite_db)

db_uri = postgres_uri  # passed to alembic

sqlite_engine = create_engine(sqlite_uri)
postgres_engine = create_engine(postgres_uri,
                                pool_size=10,
                                max_overflow=2,
                                pool_recycle=300,
                                pool_pre_ping=True,
                                pool_use_lifo=True)

sq_session = sessionmaker(bind=sqlite_engine)
pg_session = sessionmaker(bind=postgres_engine)

Session = scoped_session(pg_session)


# print("\nDB_URI: ", db_uri, "\n")

# echo_value = "-db" in sys.argv
# print("-" * 6, "SQLalchemy logging is " + str(echo_value), "-" * 6, "\n")

# import models as m
# import models_old as m_old


def create_university():
    """ create university """

    print("\ncreating university")
    universities = [
        m.University(
        id=1,
        name="Одеський національний економічний університет",
        students_number=2000,
        engine_name="mkr_api",
        engine_parameters={"api_url": "http://asu.oneu.edu.ua:1080"},
        ),
        m.University(
        id=2,
        name="Одеський національний морський університет",
        students_number=5000,
        engine_name="mkr_api",
        engine_parameters={"api_url": "http://193.189.127.179:5011"},
        ),
    ]
    pg_session.bulk_save_objects(universities)
    pg_session.commit()


def create_users():
    """" transfer users with students and teachers data """

    user_objects = []

    old_students = (
        sq_session.query(
            m_old.Student.facultyId,
            m_old.Student.facultyName,
            m_old.Student.course,
            m_old.Student.groupId,
            m_old.Student.groupName,
            m_old.User.user_id,
            m_old.User.username,
            m_old.User.time_created,
        )
        .join(m_old.User)
        .all()
    )

    print("\ncreating students")
    for user in progressbar(old_students):
        student = {
            "type": "student",
            "facultyId": user[0],
            "facultyName": user[1],
            "course": user[2],
            "groupId": user[3],
            "groupName": user[4],
        }

        user_dict = {
            "chat_id": user[5],
            "is_banned": False,
            "is_group": user[5] < 0,
            "username": user[6],
            "university_id": 1,
            "user_data": student,
            "time_registered": user[7],
        }
        new_user = m.User(**user_dict)
        user_objects.append(new_user)

    old_teachers = (
        sq_session.query(
            m_old.Teacher.departmentId,
            m_old.Teacher.departmentName,
            m_old.Teacher.teacherId,
            m_old.Teacher.teacherName,
            m_old.User.user_id,
            m_old.User.username,
            m_old.User.time_created,
        )
        .join(m_old.User)
        .all()
    )

    print("\ncreating teachers")
    for user in progressbar(old_teachers):
        teacher = {
            "type": "teacher",
            "departmentId": user[0],
            "departmentName": user[1],
            "teacherId": user[2],
            "teacherName": user[3],
        }

        user_dict = {
            "chat_id": user[4],
            "is_banned": False,
            "is_group": user[4] < 0,
            "username": user[5],
            "university_id": 1,
            "user_data": teacher,
            "time_registered": user[6],
        }
        new_user = m.User(**user_dict)
        user_objects.append(new_user)

    pg_session.add_all(user_objects)
    pg_session.commit()


def create_actions():
    """" transfer actions with keyed types """

    action_objects = []
    action_types = ["today", "tomorrow", "week", "next_week"]
    for ac_type in action_types:
        action = m.Action(name=ac_type)
        action_objects.append(action)
    pg_session.add_all(action_objects)
    pg_session.commit()

    user_action_objects = []

    action_dict = {"today": 1, "tomorrow": 2, "week": 3, "next_week": 4}
    old_user_actions = sq_session.query(m_old.Action).filter(m_old.Action.id>16024).all()
    
    print("\ncreating actions")
    for action in progressbar(old_user_actions):
        user_action = m.UserAction(
            chat_id = action.user_id,
            action = action_dict[action.comment],
            time_clicked = action.time
        )
        user_action_objects.append(user_action)
        # pg_session.add(user_action)
        # pg_session.commit()

    pg_session.add_all(user_action_objects)
    pg_session.commit()


def create_groups():
    """ create groups """

    old_groups = sq_session.query(m_old.Group).all()

    errors = 0
    print("\ncreating groups")
    for group in progressbar(old_groups):
        new_group = m.Group(chat_id=group.group_id, members_count=group.members_count)
        pg_session.add(new_group)
        try:
            pg_session.commit()
        except Exception as e:
            errors += 1
            pg_session.rollback()
            # print(e)

    print("errors: ", errors)


def create_timers():
    """ create timers """

    old_timers = sq_session.query(m_old.Timer).all()
    errors = 0

    print("\ncreating timers")
    for timer in progressbar(old_timers):
        new_timer = m.Timer(chat_id=timer.id, hour=timer.hour)
        pg_session.add(new_timer)
        try:
            pg_session.commit()
        except Exception as e:
            errors += 1
            pg_session.rollback()
            # print(e)
    print("errors: ", errors)



# m.Base.metadata.drop_all(postgres_engine)  # deletes all tables and data
# m.Base.metadata.create_all(postgres_engine)


# create_university()
# create_users()
# create_groups()
# create_timers()
# create_actions()


# sq_session.close()
# pg_session.close()