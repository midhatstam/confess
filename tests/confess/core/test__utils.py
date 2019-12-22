import datetime
from collections import namedtuple

from django.test import TestCase

from confession.utils import DateTimeService
from rule.models import Rule


class DateTimeServiceTest(TestCase):
    def setUp(self) -> None:
        start_time = Rule(name='Exec start time', value='09:00', slug='exec-start-time')
        end_time = Rule(name='Exec end time', value='15:00', slug='exec-end-time')
        Rule.objects.bulk_create([start_time, end_time])

        self.datetime_now = datetime.datetime.now()
        self.datetime_one_hour = self.datetime_now - datetime.timedelta(hours=1)
        self.datetime_one_day = self.datetime_now - datetime.timedelta(days=1)

    def test__start_time(self):
        self.assertEqual(3, Rule.objects.count())

        start_time_service = DateTimeService.get_start_time()
        expected_time = datetime.time(9, 0)
        self.assertEqual(expected_time, start_time_service)

    def test__end_time(self):
        self.assertEqual(3, Rule.objects.count())

        end_time_service = DateTimeService.get_end_time()
        expected_time = datetime.time(15, 0)
        self.assertEqual(expected_time, end_time_service)

    def test__get_execution_times(self):
        self.assertEqual(3, Rule.objects.count())

        Time = namedtuple('Time', 'start end')

        get_exec_time_service = DateTimeService.get_execution_times()
        expected_time = Time(start=datetime.time(9, 0), end=datetime.time(15, 0))
        self.assertEqual(expected_time, get_exec_time_service)

    def test__get_random_time(self):
        self.assertEqual(3, Rule.objects.count())

        get_random_time_service = DateTimeService.get_random_time()
        self.assertTrue(isinstance(get_random_time_service, datetime.datetime))

    def test__get_date_now(self):
        get_date_service_now = DateTimeService.get_date(self.datetime_now)
        expected_date_now = 'az önce'
        self.assertEqual(expected_date_now, get_date_service_now)

    def test__get_date_hour(self):
        get_date_service_hour = DateTimeService.get_date(self.datetime_one_hour)
        expected_date_hour = '1 saat önce'
        self.assertEqual(expected_date_hour, get_date_service_hour)


class DateTimeServiceNoSetUpTest(TestCase):

    def test__get_execution_times(self):
        self.assertEqual(1, Rule.objects.count())

        Time = namedtuple('Time', 'start end')

        get_exec_time_service = DateTimeService.get_execution_times()
        expected_time = Time(start=datetime.time(9, 0), end=datetime.time(15, 0))
        self.assertEqual(expected_time, get_exec_time_service)
