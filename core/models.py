from django.db import models


class ItemMetaData(models.Model):
    class Meta:
        db_table = "item_meta_data"
        abstract = True

    item_meta_data_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
