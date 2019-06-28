from django import template

from core.models import Comment

register = template.Library()


@register.simple_tag
def get_commments_count(confess_id):
	return Comment.objects.filter(comment_related=confess_id).count()
