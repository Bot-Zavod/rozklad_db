""" playgroud to tinker with DB requests """

from models import *

from datetime import datetime, timedelta
from dateutil import tz

from sqlalchemy.sql import func


def new_actions():
    kiev_tz = tz.gettz("Europe/Kiev")
    current_time = datetime.now(kiev_tz)
    day_ago = current_time - timedelta(days=30)

    new_actions = session.query(Action).filter(Action.time > day_ago)
    total_users = new_actions.distinct(Action.user_id).group_by(Action.user_id).count()

    news_msg = f"{total_users} юзеров сделали {new_actions.count()} запросов:\n"

    print(news_msg)

    session.close()
    
if __name__ == "__main__":
    new_actions()    
    