from django.contrib import admin

from confession.models import Confession


class ConfessionAdmin(admin.ModelAdmin):
	exclude = ("css_class",)


admin.site.register(Confession, ConfessionAdmin)
