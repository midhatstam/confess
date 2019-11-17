import datetime
import random
import json
import logging

from django.conf import settings
from django.http import HttpResponse
from InstagramAPI import InstagramAPI as Insta

from core.package import post

logger = logging.getLogger(__name__)


def get_random_time():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    tomorrow_start = datetime.datetime.combine(tomorrow, datetime.time(9, 0)).timestamp()
    tomorrow_end = datetime.datetime.combine(tomorrow, datetime.time(15, 00)).timestamp()

    random_time = random.randint(tomorrow_start, tomorrow_end)
    random_time_human = datetime.datetime.fromtimestamp(random_time)
    return random_time_human


def instagram(request):
    InstagramAPI = Insta("+905393205773", "konfess1453")
    InstagramAPI.login()

    photo_path = settings.BASE_DIR + '/static/img/theme/team-4-800x800.jpg'
    caption = "Sample photo"
    response = InstagramAPI.uploadPhoto(photo_path, caption=caption)
    print(response)
    return HttpResponse(json.dumps(str(response)), content_type="application/json")


def slack_notify(message):
    # slack = Slacker(app_settings.SLACK_TOKEN)
    # if slack.api.test().successful:
    #     print(
    #         f"Connected to {slack.team.info().body['team']['name']}.")
    # else:
    #     print('Try Again!')
    # slack.chat.post_message(channel='#tasks', text=message, username='Task worker', icon_emoji=':construction_worker:')

    data = {
        'channel': settings.SLACK_CHANNEL,
        'username': settings.SLACK_USERNAME,
        'mrkdwn': True,
        'text': message,
        'link_names': 1,
    }

    try:
        response = post(
            url=settings.SLACK_WEBHOOK,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
    except Exception as e:
        response = None
        logger.debug(f'Cound not send slack message')
        logger.exception(e)

    return response
