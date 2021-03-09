""" playgroud to tinker with DB requests """

from dotenv import load_dotenv

load_dotenv()

from models import *
from models import Session as session

from datetime import datetime, timedelta

from sqlalchemy.sql import func

from progressbar import progressbar

def new_actions():
    chat_id = 384341805
    users = session.query(User).all()
    for user in progressbar(users):
        user.is_banned = True
    session.commit()
    session.close()


if __name__ == "__main__":
    new_actions()
