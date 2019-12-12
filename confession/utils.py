import datetime
import random
import json
import logging
import uuid
from collections import namedtuple

from django.conf import settings
from django.http import HttpResponse
from InstagramAPI import InstagramAPI as Insta
from django.utils.timesince import timesince

from core.package import post
from rule.models import Rule

logger = logging.getLogger(__name__)


class DateTimeService:
    @classmethod
    def get_start_time(cls):
        try:
            execution_range_start_time = Rule.objects.get(slug='exec-start-time')
        except Rule.DoesNotExist as err:
            return err

        return datetime.datetime.strptime(execution_range_start_time, '%H:%M').time()

    @classmethod
    def get_end_time(cls):
        try:
            execution_range_end_time = Rule.objects.get(slug='exec-end-time')
        except Rule.DoesNotExist as err:
            return err

        return datetime.datetime.strptime(execution_range_end_time, '%H:%M').time()

    @classmethod
    def get_execution_times(cls):
        time_tuple = namedtuple('Time', 'start, end')
        try:
            return time_tuple(start=cls.get_start_time(), end=cls.get_end_time())
        except Exception as err:
            logger.warning(
                f'Could not create one of execution time. Possibly "exec-start-time" or "exec-end-time" not found in db!')
            logger.exception(err)

            start_time = datetime.datetime.strptime('09:00', '%H:%M').time()
            end_time = datetime.datetime.strptime('15:00', '%H:%M').time()
            logger.warning(f'Execution time using default values as: start=09:00 and end=15:00')
            return time_tuple(start=start_time, end=end_time)

    @classmethod
    def get_random_time(cls):
        times = cls.get_execution_times()
        now_hour = datetime.datetime.now().time()
        if now_hour < times.start:
            execute_date = datetime.date.today()
        else:
            execute_date = datetime.date.today() + datetime.timedelta(days=1)
        tomorrow_start = datetime.datetime.combine(execute_date, times.start).timestamp()
        tomorrow_end = datetime.datetime.combine(execute_date, times.end).timestamp()

        random_time = random.randint(tomorrow_start, tomorrow_end)
        random_time_human = datetime.datetime.fromtimestamp(random_time)
        return random_time_human

    @classmethod
    def get_date(cls, date):
        from django.utils import translation
        translation.activate('tr')
        now = datetime.datetime.now()
        # date_obj = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S.%f')

        try:
            difference = now - date.replace(tzinfo=None)
        except:
            return date

        if difference <= datetime.timedelta(minutes=1):
            return "az önce"
        elif difference >= datetime.timedelta(days=1):
            return date.strftime("%d %b %Y")
        else:
            return "%(time)s önce" % {'time': timesince(date).split(', ')[0]}


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


def verify_token_version(token):
    if uuid.UUID(token).version is not 4:
        raise ValueError
    return True
