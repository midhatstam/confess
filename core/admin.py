from django.contrib import admin
from core.models import Confess, Comment
# Register your models here.


class ConfessAdmin(admin.ModelAdmin):
	exclude = ("confess_class", )
	

admin.site.register(Confess, ConfessAdmin)
admin.site.register(Comment)
