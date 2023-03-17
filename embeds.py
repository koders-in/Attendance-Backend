from slack_webhook import Slack
from redmine import get_user_data
import os

WEBHOOK_URL = os.getenv('WEBHOOK_URL')

def send_webhook(url, username, position, issues, hours, thumbnail_url, color):
    if color == 'green':
        color = 'good'
    else:
        color = 'danger'

    slack = Slack(url=url)
    response = slack.post(
        attachments = [{
            "fallback": "Attendance Marked",
            "author_name": "Redmine marked an attendance",
            "title": "User",
            "text": username,
            "color": color,
            "actions": [
                {
                    "name": "action",
                    "type": "button",
                    "text": "Check attendance",
                    "style": "",
                    "value": "complete",
                    "url": "https://attendance.koders.in"
                },
            ],
                "fields": [
                    {
                        "title": "Position",
                        "value": position,
                        "short": False
                    },
                    {
                        "title": "Issues",
                        "value": issues,
                        "short": True
                    },
                    {
                        "title": "Spent time",
                        "value": str(hours),
                        "short": True
                    }
                ],
            "thumb_url": thumbnail_url,
        }]
    )
    print(response)

def create_webhook(user_id, color):
    username, position, opened_issues, total_issues, hours, thumbnail_url = get_user_data(user_id)
    issues = str(opened_issues) + "/" + str(total_issues)
    send_webhook(WEBHOOK_URL, username, position, issues, hours, thumbnail_url, color)
