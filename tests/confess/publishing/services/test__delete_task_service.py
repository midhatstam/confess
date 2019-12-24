import datetime

from django.test import TestCase
from django_celery_beat.models import PeriodicTask, ClockedSchedule

from publishing.services.delete_task_service import DeleteTaskService


class DeleteTaskServiceTest(TestCase):
    def setUp(self) -> None:
        clocked = ClockedSchedule.objects.create(
            clocked_time=datetime.datetime.now() - datetime.timedelta(hours=1)
        )
        PeriodicTask.objects.create(
            clocked=clocked,
            enabled=False,
            name='periodic_task_test',
            one_off=True
        )

    def test__delete_task_service(self):
        current_periodic_task = PeriodicTask.objects.count()
        expected_periodic_task = 1
        self.assertEqual(expected_periodic_task, current_periodic_task)

        DeleteTaskService.delete()

        periodic_task_after_service = PeriodicTask.objects.count()
        expected_periodic_task_after_service = 0
        self.assertEqual(expected_periodic_task_after_service, periodic_task_after_service)

    def test__delete_only_old_task_service(self):
        current_periodic_task = PeriodicTask.objects.count()
        expected_periodic_task = 1
        self.assertEqual(expected_periodic_task, current_periodic_task)

        clocked = ClockedSchedule.objects.create(
            clocked_time=datetime.datetime.now()
        )
        PeriodicTask.objects.create(
            clocked=clocked,
            enabled=False,
            name='periodic_task_test_2',
            one_off=True
        )

        DeleteTaskService.delete()

        periodic_task_after_service = PeriodicTask.objects.count()
        expected_periodic_task_after_service = 1
        self.assertEqual(expected_periodic_task_after_service, periodic_task_after_service)
