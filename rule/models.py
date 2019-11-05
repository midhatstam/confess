from django.db import models


class Rule(models.Model):
    class Meta:
        db_table = "rule"

    name = models.CharField(max_length=250, blank=False, null=False)
    app = models.CharField(max_length=100, blank=False, null=False)
    model = models.CharField(max_length=100, blank=False, null=False)
    value = models.IntegerField()
