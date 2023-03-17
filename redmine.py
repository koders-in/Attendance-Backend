from redminelib import Redmine
import libgravatar
import datetime
import requests
import json
import os


def get_profile_picture(user_email):
    return libgravatar.Gravatar(user_email).get_image()


def get_user_data(user_id):
    redmine = Redmine('https://kore.koders.in', key=os.getenv('API_KEY'))

    user = redmine.user.get(user_id)
    for x in user:
        print(x)
    position = (user['custom_fields'][1]['value'])
    issues = redmine.issue.all(limit=10000, assigned_to_id=user_id)
    opened_issues, total_issues = 0, 0
    for issue in issues:
        if str(issue.status) != 'Closed':
            opened_issues += 1
        total_issues += 1

    week = []
    for i in range(0, 7):
        week.append(((datetime.datetime.now() - datetime.timedelta(days=i)).date()))

    hours = 0
    for day in week:
        time_entries = redmine.time_entry.filter(user_id=user_id, spent_on=day)
        for x in time_entries:
            hours += x.hours

    profile_picture = get_profile_picture(user.mail)
    return str(user['firstname'] + " "+ user['lastname']), position, opened_issues, total_issues, hours, profile_picture
