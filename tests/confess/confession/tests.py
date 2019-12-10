import uuid

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIRequestFactory

from confession.models import Confession, ConfessionUserApprovement
from confession import views as confession_views


class ReversedUrls:
    @classmethod
    def get_send_approvement_url(cls):
        return reverse('send-approvement')


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
        self.send_approvement_url = ReversedUrls.get_send_approvement_url()
        self.factory = APIRequestFactory()

    def test__approvement(self):
        ConfessionUserApprovement.objects.create(
            confession=self.create_confession(),
            vote=1,
            token=self.token
        )

        confession_approvement_count = Confession.objects.prefetch_related("confessionuserapprovement_set").count()

        self.assertEqual(confession_approvement_count, 1)

    def test__approvement_api(self):
        self.confession = self.create_confession()
        req = self.factory.post(
            self.send_approvement_url,
            {"confession": self.confession.id, "vote": 1},
        )
        req.COOKIES['session_token'] = self.token

        resp = confession_views.ConfessionUserApprovementView.as_view({'post': 'create'})(req)

        self.assertTrue(resp.data)

        approvement = ConfessionUserApprovement.objects.first()

        self.assertEqual(approvement.id, 1)
        self.assertTrue(approvement.token)

    def test__approvement_api_wrong_token(self):
        with self.assertRaises(ValueError) as err:
            self.confession = self.create_confession()
            req = self.factory.post(
                self.send_approvement_url,
                {"confession": self.confession.id, "vote": 1},
            )
            req.COOKIES['session_token'] = '1a6ae4ce-1a58-11ea-978f-2e728ce88125'

            resp = confession_views.ConfessionUserApprovementView.as_view({'post': 'create'})(req)

            version = uuid.UUID(req.COOKIES['session_token']).version

            self.assertEqual(resp, 2)
            self.assertEqual(version, 1)
