from django.db import models
from django.utils.text import slugify


class Rule(models.Model):
    class Meta:
        db_table = "rule"

    name = models.CharField(max_length=250, blank=False, null=False)
    slug = models.SlugField(unique=True, blank=True, null=True)
    app = models.CharField(max_length=100, blank=False, null=False)
    model = models.CharField(max_length=100, blank=False, null=False)
    value = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.name is not '':
            self.slug = slugify(self.name)

        super(Rule, self).save(*args, **kwargs)
