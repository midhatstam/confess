from django.contrib.auth.models import User
from django.db import models

from confession.models import Confession
from comment.models import Comment
from core.models import ItemMetaData


class ReportComment(ItemMetaData):
    class Meta:
        db_table = 'report_comment'

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="comments")
    reason = models.TextField(blank=False, null=False)
