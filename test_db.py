""" playgroud to tinker with DB requests """

from dotenv import load_dotenv

load_dotenv()

from models import *
from models import Session as session

from datetime import datetime, timedelta
from dateutil import tz

from sqlalchemy.sql import func


def new_actions():
    chat_id = 384341805
    university_id, user_data = (
        session.query(User.university_id, User.user_data)
        .filter(User.chat_id == chat_id)
        .first()
    )
    session.close()
    print(university_id, user_data)


if __name__ == "__main__":
    new_actions()
