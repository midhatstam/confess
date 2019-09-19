from django import template

from datetime import datetime, timedelta
from django.utils.timesince import timesince


register = template.Library()


@register.simple_tag
def get_date(date):
	now = datetime.now()
	date_obj = datetime.strptime(date, '%d.%m.%Y %H:%M:%S.%f')
	
	try:
		difference = now - date_obj.replace(tzinfo=None)
	except:
		return date
	
	if difference <= timedelta(minutes=1):
		return "just now"
	elif difference >= timedelta(days=1):
		return date_obj.strftime("%d %b %Y")
	else:
		return "%(time)s ago" % {'time': timesince(date_obj).split(', ')[0]}
