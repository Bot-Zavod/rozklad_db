""" playgroud to tinker with DB requests """

from dotenv import load_dotenv

load_dotenv()

from models import *
from models import Session as session

from datetime import datetime, timedelta

from sqlalchemy.sql import func
from sqlalchemy import desc

from progressbar import progressbar
from colorama import init, Fore

init(autoreset=True)


def university_segments(university_id=2):

    users = (
        session.query(User.user_data)
        .filter(User.is_banned == False)
        .filter(User.university_id == university_id)
        .filter(User.user_data["type"].astext == "student")
        .all()
    )
    uni_name = session.query(University).get(university_id).name

    stract = {}
    for user in users:
        user = user[0]

        faculty = user["facultyName"]
        course = user["course"]

        if faculty not in stract:
            stract[faculty] = [{course: 1}, 1]
        else:
            stract[faculty][1] += 1

            if course not in stract[faculty][0]:
                stract[faculty][0][course] = 1
            else:
                stract[faculty][0][course] += 1

    stract = sorted(stract.items(), key=lambda x: x[1][1], reverse=True)
    print(uni_name, " ", Fore.RED + str(len(users)) + " people\n")
    for fack, num in stract:
        print(Fore.RED + str(num[1]), fack)
        courses = sorted(num[0].items(), key=lambda x: x[1], reverse=True)
        for course, i in courses:
            print("\t", Fore.RED + str(i), course, "corse")

    session.close()


def active_users(university_id=2):
    # select count( user_action.chat_id ), u.username
    #     from user_action
    #     join "user" u on u.chat_id = user_action.chat_id
    #     where u.university_id = 2
    #         group by u.chat_id
    #     order by count( user_action.chat_id ) desc
    #     limit 10
    users = (
        session.query(func.count(UserAction.chat_id), User.username)
        .join(User)
        .group_by(UserAction.chat_id, User.chat_id)
        .order_by(desc(func.count(UserAction.chat_id)))
        .filter(User.username != None)
        .filter(User.university_id == university_id)
        .limit(30)
    )
    for user in users[9:]:
        print(user[0], " @" + user[1])


if __name__ == "__main__":
    print()
    # university_segments()
    active_users()
    print()
