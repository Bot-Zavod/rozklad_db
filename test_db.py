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
    act = session.query(UserAction).get(50000)
    session.close()
    print(act)


if __name__ == "__main__":
    new_actions()
