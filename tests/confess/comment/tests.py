import uuid

from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory, APITestCase
from django.urls import reverse

from comment import views as comment_views
from comment.models import Comment

from tests.confess.confession.tests import CreateConfessionTest


class ReversedUrls:

    @classmethod
    def get_comments_url(cls):
        return reverse('comments', kwargs={'id': 1})

    @classmethod
    def get_reply_url(cls):
        return reverse('comment-replies', kwargs={'id': 1, 'comment_id': 1})


class CommentTest(CreateConfessionTest, APITestCase):
    def setUp(self) -> None:
        self.username = 'John'
        self.body = 'Hello'
        self.related = self.create_confession()
        self.comment_url = ReversedUrls.get_comments_url()
        self.factory = APIRequestFactory()
        self.is_parent = True

    def create_comment(self):
        comment = Comment.objects.create(
            username='Alex',
            body='Comment',
            is_parent=True,
            related_id=self.related.id
        )
        return comment

    def test__create_comment(self):
        req = self.factory.post(
            self.comment_url,
            {'username': 'Alex', 'body': 'Comment', 'is_parent': self.is_parent},
        )
        req.COOKIES.setdefault('session_token', str(uuid.uuid4()))

        resp = comment_views.CommentApiMixin.as_view({'post': 'create'})(req, id=self.related.id)

        comment_count = Comment.objects.all().count()

        self.assertTrue(
            resp.data['id']
        )
        self.assertTrue(
            resp.data['is_parent']
        )
        self.assertTrue(
            comment_count, 1
        )

    def test__list_comments(self):
        self.comment = self.create_comment()
        req = self.factory.get(
            self.comment_url
        )
        req.COOKIES.setdefault('session_token', str(uuid.uuid4()))

        resp = comment_views.CommentApiMixin.as_view({'get': 'list'})(req, id=self.related.id)

        comment_count = Comment.objects.all().count()

        self.assertTrue(
            resp.data[0]['id']
        )
        self.assertTrue(
            resp.data[0]['is_parent']
        )
        self.assertTrue(
            comment_count, 1
        )


class CommentReply(CreateConfessionTest, APITestCase):

    def setUp(self) -> None:
        self.related = self.create_confession()
        self.is_parent = False
        self.parent = self.create_comment()
        self.factory = APIRequestFactory()
        self.reply_url = ReversedUrls.get_reply_url()

    def create_comment(self):
        comment = Comment.objects.create(
            username='Alex',
            body='Comment',
            is_parent=True,
            related_id=self.related.id
        )
        return comment

    def create_reply(self):
        reply = Comment.objects.create(
            username='Bob',
            body='Hello Alex',
            is_parent=False,
            related_id=self.related.id,
            parent_id=self.comment.id
        )
        return reply

    def test__create_reply(self):
        req = self.factory.post(
            self.reply_url,
            {'username': 'Bob', 'body': 'Hi Alex'}
        )
        req.COOKIES.setdefault('session_token', str(uuid.uuid4()))

        resp = comment_views.CommentDetailsApiMixin.as_view({
            'post': 'create'
        })(
            req,
            id=self.related.id,
            comment_id=self.parent.id
        )

        comment_count = Comment.objects.all().count()

        self.assertIsNotNone(
            resp.data['parent']
        )
        self.assertFalse(
            resp.data['is_parent']
        )
        self.assertTrue(
            comment_count, 2
        )

    def test__list_replies(self):
        self.comment = self.create_comment()
        self.reply = self.create_reply()

        req = self.factory.get(
            self.reply_url
        )
        req.COOKIES.setdefault('session_token', str(uuid.uuid4()))

        resp = comment_views.CommentDetailsApiMixin.as_view({'get': 'list'})(req, id=self.related.id,
                                                                             comment_id=self.comment.id)

        comment_count = Comment.objects.all().count()

        self.assertIsNotNone(
            resp.data[0]['parent']
        )
        self.assertFalse(
            resp.data[0]['is_parent']
        )
        self.assertTrue(
            comment_count, 2
        )

    def test__list_replies_wrong_releated(self):
        self.comment = self.create_comment()
        self.reply = self.create_reply()

        req = self.factory.get(
            self.reply_url
        )
        req.COOKIES.setdefault('session_token', str(uuid.uuid4()))

        resp = comment_views.CommentDetailsApiMixin.as_view({'get': 'list'})(req, id=(self.related.id + 10),
                                                                             comment_id=self.comment.id)

        self.assertEqual(200, resp.status_code)
        self.assertRaises(ValidationError)
