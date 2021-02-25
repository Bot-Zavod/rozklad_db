from .models import User, Group, UserAction, Action
from .base import Session as session


# r1 = session.query(Student).join(User).all()

# for row in r1:
#     print(row, row.user)
# print ("userId: ", row.User.userId, "facultyId: ", row.Student.facultyId)

# print(r1.userId, r1.username, r1.facultyId)


# returns boolean if obj exists in table
# session.query(exists().where(User.user_id==1)).scalar()

"""

user_type:
1 - blank
2 - student
3 - teacher

action_type
1 - group_schedule
2 - teacher_schedule

"""


def add_user(chat_id, username):
    """
    Create user record if not exist, otherwise update username
    """
    user = session.query(User).get(chat_id)
    if user:
        if user.username != username:
            user.username = username
            session.commit()
    else:
        new_user = User(chat_id=chat_id, username=username, user_type=1)
        session.add(new_user)
        session.commit()
    session.close()


def add_group(chat_id, members_count):
    group = session.query(Group).get(chat_id)

    if group:
        if group.members_count != members_count:
            group.members_count = members_count
            session.commit()
    else:
        group = Group(group_id=chat_id, members_count=members_count)
        session.add(group)
        session.commit()
    session.close()


def user_is_registered(chat_id):
    """
    Create user record if not exist, otherwise update username
    """
    user = session.query(User).get(chat_id)
    session.close()
    if user.user_data:
        return True
    return False


def add_user_data(chat_id, university_id, data):
    user = session.query(User).get(chat_id)
    user.university_id = university_id
    user.user_data = data
    session.commit()
    session.close()


def log_action(chat_id, action):
    action_type = session.query(Action).filter(Action.name==action).first()
    new_action = UserAction(chat_id=chat_id, action=action_type.id)
    session.add(new_action)
    session.commit()
    session.close()
