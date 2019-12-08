from django.contrib import admin

from confession.models import Confession


class ConfessionAdmin(admin.ModelAdmin):
	fields = '__all__'


admin.site.register(Confession, ConfessionAdmin)
