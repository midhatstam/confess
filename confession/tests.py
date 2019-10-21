from django.test import TestCase, override_settings
from django.utils import timezone

from confession.models import Confession


@override_settings(ALLOWED_HOSTS=["localhost", "127.0.0.1", "[::1]"])
class ConfessionTest(TestCase):
    def setUp(self):
        Confession.objects.create(body='Testing....', item_meta_data_date=timezone.now(), admin_approved=1)

    def test__confession_is_posted(self):
        confession1 = Confession.objects.filter().first()
        self.assertEqual(confession1.id, 1)
