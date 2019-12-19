import logging

from django.db.models import Sum, Case, When, IntegerField

from confession.models import AdminApprovedConfession
from confession.utils import DateTimeService, slack_notify
from rule.models import Rule

logger = logging.getLogger(__name__)


class SetPublishTime:

    @classmethod
    def get_instances(cls):
        approved_limit_rule = int(Rule.objects.get(slug='approve-confession').value)
        instances = AdminApprovedConfession.objects.filter(publish_date__isnull=True, user_approved=False).annotate(
            approved_count=Sum(
                Case(
                    When(confessionuserapprovement__vote=True, then=1),
                    When(confessionuserapprovement__vote=False, then=-1),
                    When(confessionuserapprovement=None, then=0),
                    output_field=IntegerField()
                )
            )
        ).filter(approved_count__gte=approved_limit_rule).order_by('-approved_count')

        logger.debug(f'Filtered confession queryset is: {instances}')
        return instances

    def update(self, instances, *args, **kwargs):
        if instances.exists():
            for confession in instances:
                publish_time = DateTimeService.get_random_time()
                try:
                    confession.publish_date = publish_time
                    confession.save()
                    message = f'Confession with id: {confession.id} and approved votes: {confession.approved_count} updated with publish_time of {publish_time}'
                    slack_notify(message=message)
                except Exception as e:
                    message = f'Confession with id: {confession.id} could not be updated with publish_time of {publish_time} with error: {e}'
                    slack_notify(message=message)
                    continue
            return f'Task executed with confessions: {instances}'
        else:
            message = 'There is no confession to publish'
            slack_notify(message=message)

            return f'Task executed with message: {message}'
