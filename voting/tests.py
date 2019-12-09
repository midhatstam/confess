import uuid
from http.cookies import SimpleCookie

from django.urls import reverse
from rest_framework.test import APIRequestFactory

from comment.tests import CommentTest
from confession.tests import CreateConfessionTest
from voting import views as voting_views


class ReversedUrls:
    @classmethod
    def get_voting_url(cls):
        return reverse('vote')


class VoteConfession(CreateConfessionTest):
    def setUp(self) -> None:
        self.token = uuid.uuid4()
        self.voting_url = ReversedUrls.get_voting_url()
        self.factory = APIRequestFactory()
        self.confession = self.create_confession()
        self.related = self.confession
        self.comment = CommentTest.create_comment(self)

    def test__vote_confession_api(self):
        req = self.factory.post(
            self.voting_url,
            {"vote": "true", "model": "confession", "id": self.confession.id},
        )
        req.COOKIES['session_token'] = self.token

        resp = voting_views.VoteMixin.as_view({'post': 'up'})(req)

        self.assertEqual(resp.data['success'], 'true')
        self.assertEqual(resp.data['message'], 'created')
        self.assertEqual(resp.data['likes'], 1)

    def test__vote_comment_api(self):
        req = self.factory.post(
            self.voting_url,
            {"vote": "false", "model": "comment", "id": self.comment.id}
        )
        req.COOKIES['session_token'] = self.token
        resp = voting_views.VoteMixin.as_view({'post': 'up'})(req)

        self.assertEqual(resp.data['success'], 'true')
        self.assertEqual(resp.data['message'], 'created')
        self.assertEqual(resp.data['dislikes'], 1)
