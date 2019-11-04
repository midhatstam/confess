import datetime
import random
import json

from django.conf import settings
from django.http import HttpResponse
from InstagramAPI import InstagramAPI as Insta


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