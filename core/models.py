from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.BigIntegerField(verbose_name='ВК id', editable=False, primary_key=True)
