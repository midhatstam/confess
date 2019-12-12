from django.db import models
from django.utils.text import slugify


class Rule(models.Model):
    class Meta:
        db_table = "rule"

    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True, null=True)
    app = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    value = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Rule, self).save(*args, **kwargs)
