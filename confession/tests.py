import uuid

from django.test import TestCase, override_settings
from django.utils import timezone

from confession.models import Confession, ConfessionUserApprovement


@override_settings(ALLOWED_HOSTS=["localhost", "127.0.0.1", "[::1]"])
class CreateConfessionTest(TestCase):
    def create_confession(self):
        Confession.objects.create(body='Testing....', item_meta_data_date=timezone.now(), admin_approved=1).save()
        confession = Confession.objects.all().first()
        confession_count = Confession.objects.all().count()

        self.assertEqual(confession_count, 1)
        return confession


class ConfessionTest(CreateConfessionTest):
    def test__confession_is_posted(self):
        confession = self.create_confession()
        self.assertEqual(confession.id, 1)


class ConfessionUserApprovementTest(CreateConfessionTest):
    def setUp(self):
        self.token = uuid.uuid4()

    def test__approvement(self):
        ConfessionUserApprovement.objects.create(
            confession=self.create_confession(),
            vote=1,
            token=self.token
        )

        confession_approvement_count = Confession.objects.prefetch_related("confessionuserapprovement_set").count()

        self.assertEqual(confession_approvement_count, 1)
